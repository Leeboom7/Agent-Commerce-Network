"""Tests for reputation system."""

from datetime import datetime, timedelta, timezone

from acp.protocol.models import Rating
from acp.reputation.ratings import ReputationEngine
from acp.reputation.trust import TrustGraph


class TestReputationEngine:
    @property
    def engine(self) -> ReputationEngine:
        return ReputationEngine(half_life_days=90.0)

    def test_new_agent_neutral_score(self) -> None:
        rep = self.engine.get_reputation("new-agent")
        assert rep.composite_score == 100.0
        assert rep.total_transactions == 0

    def test_submit_rating_increases_transactions(self) -> None:
        e = self.engine
        e.submit_rating_direct(
            "agent-a", "rater-1", "txn-1",
            scores={"quality": 5.0, "timeliness": 4.0, "communication": 5.0},
        )
        rep = e.get_reputation("agent-a")
        assert rep.total_transactions == 1
        assert rep.successful_transactions == 1

    def test_submit_bad_rating(self) -> None:
        e = self.engine
        e.submit_rating_direct(
            "agent-a", "rater-1", "txn-1",
            scores={"quality": 1.0, "timeliness": 1.0},
        )
        rep = e.get_reputation("agent-a")
        assert rep.total_transactions == 1
        assert rep.successful_transactions == 0  # below 3.0 threshold
        assert rep.composite_score < 100.0

    def test_time_decay(self) -> None:
        e = ReputationEngine(half_life_days=30.0)

        # Submit an old rating
        old_rating = Rating(
            rater_id="rater-1",
            transaction_id="txn-1",
            scores={"quality": 5.0, "timeliness": 5.0},
            timestamp=datetime.now(timezone.utc) - timedelta(days=60),
        )
        # Manually add to record
        rec = e._get_or_create_record("agent-b")
        rec.ratings.append(old_rating)
        rec.total_transactions += 1
        rec.successful_transactions += 1
        rec.composite_score = e._compute_composite(rec)

        # Submit a fresh rating
        e.submit_rating_direct(
            "agent-b", "rater-2", "txn-2",
            scores={"quality": 1.0, "timeliness": 1.0},
        )

        rep = e.get_reputation("agent-b")
        # Fresh bad rating should pull down the score significantly
        # even though the old rating was perfect
        assert rep.composite_score < 100.0

    def test_multiple_ratings_average(self) -> None:
        e = self.engine
        for i in range(3):
            e.submit_rating_direct(
                "agent-c", f"rater-{i}", f"txn-{i}",
                scores={"quality": 4.0, "timeliness": 4.0},
            )
        rep = e.get_reputation("agent-c")
        assert rep.total_transactions == 3
        # Score should be high (4.0 avg → 80 + success bonus)
        assert rep.composite_score >= 70.0

    def test_volume_regression_for_new_agents(self) -> None:
        e = self.engine
        # Only 1 transaction → volume factor 0.2
        e.submit_rating_direct(
            "agent-d", "rater-1", "txn-1",
            scores={"quality": 5.0, "timeliness": 5.0},
        )
        rep = e.get_reputation("agent-d")
        # With volume_factor=0.2, score = 100*0.2 + 50*0.8 + success_bonus
        # ≈ 60 + bonus, should be moderated
        assert rep.composite_score < 100.0

    def test_get_top_agents(self) -> None:
        e = self.engine
        e.submit_rating_direct("high", "r", "t1", {"quality": 5.0})
        e.submit_rating_direct("high", "r", "t2", {"quality": 5.0})
        e.submit_rating_direct("mid", "r", "t3", {"quality": 3.0})
        e.submit_rating_direct("low", "r", "t4", {"quality": 1.0})

        top = e.get_top_agents(min_transactions=1, limit=3)
        assert len(top) == 3
        assert top[0][0] == "high"  # Highest score first


class TestTrustGraph:
    @property
    def graph(self) -> TrustGraph:
        g = TrustGraph()
        g.set_trust("A", "B", 0.9)
        g.set_trust("B", "C", 0.8)
        g.set_trust("A", "D", 0.5)
        g.set_trust("D", "C", 0.6)
        return g

    def test_direct_trust(self) -> None:
        assert self.graph.get_direct_trust("A", "B") == 0.9
        assert self.graph.get_direct_trust("A", "C") is None

    def test_set_trust_clamps(self) -> None:
        g = TrustGraph()
        g.set_trust("A", "B", 1.5)
        assert g.get_direct_trust("A", "B") == 1.0
        g.set_trust("A", "B", -0.5)
        assert g.get_direct_trust("A", "B") == 0.0

    def test_transitive_trust(self) -> None:
        # A→B (0.9) → C (0.8): path trust = 0.72
        # A→D (0.5) → C (0.6): path trust = 0.30
        # Weighted avg (two equal-length paths): (0.72+0.30)/2 = 0.51
        trust = self.graph.compute_transitive_trust("A", "C")
        assert trust is not None
        assert 0.4 < trust < 0.7  # ~0.51

    def test_transitive_self_trust(self) -> None:
        trust = self.graph.compute_transitive_trust("A", "A")
        assert trust == 1.0

    def test_no_path(self) -> None:
        trust = self.graph.compute_transitive_trust("A", "Z")
        assert trust is None

    def test_update_trust(self) -> None:
        g = TrustGraph()
        g.update_trust("A", "B", +0.1)
        assert g.get_direct_trust("A", "B") == 0.6  # default 0.5 + 0.1
        g.update_trust("A", "B", -0.3)
        assert g.get_direct_trust("A", "B") == 0.3  # 0.6 - 0.3

    def test_most_trusted(self) -> None:
        top = self.graph.get_most_trusted("A", limit=2)
        assert len(top) == 2
        assert top[0] == ("B", 0.9)

    def test_graph_stats(self) -> None:
        # 4 agents: A, B, C, D. C has no outgoing edges but is in the graph
        assert self.graph.agent_count >= 3
        assert self.graph.edge_count == 4
