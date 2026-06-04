"""Tests for negotiation engine and strategies."""

import pytest

from acp.negotiation.engine import NegotiationEngine, OutcomeType
from acp.protocol.models import MarketContext
from acp.negotiation.strategies import (
    BATNAStrategy,
    ConcessionStrategy,
    TitForTatStrategy,
    ValueBasedStrategy,
    create_strategy,
)
from acp.protocol.models import ContractTerms


class TestMarketContext:
    def test_defaults(self) -> None:
        ctx = MarketContext()
        assert ctx.counterparty_reputation == 100.0
        assert ctx.market_power == 0.0

    def test_market_power_seller(self) -> None:
        ctx = MarketContext(demand_level=0.8, supply_level=0.2)
        assert ctx.market_power > 0

    def test_market_power_buyer(self) -> None:
        ctx = MarketContext(demand_level=0.2, supply_level=0.8)
        assert ctx.market_power < 0


class TestTitForTatStrategy:
    def test_initial_offer(self) -> None:
        s = TitForTatStrategy(reservation_price=50.0)
        offer = s.generate_initial_offer(MarketContext())
        assert offer.price == 75.0  # 50 * 1.5

    def test_initial_offer_with_market_avg(self) -> None:
        s = TitForTatStrategy(reservation_price=50.0)
        ctx = MarketContext(average_price=80.0)
        offer = s.generate_initial_offer(ctx)
        assert offer.price == 96.0  # 80 * 1.2

    def test_accept_good_offer(self) -> None:
        s = TitForTatStrategy(reservation_price=50.0)
        offer = ContractTerms(price=60.0)  # > 50 * 0.9 = 45
        decision = s.evaluate_offer(offer, MarketContext(), 1)
        assert decision["action"] == "accept"

    def test_counter_low_offer(self) -> None:
        s = TitForTatStrategy(reservation_price=100.0, opening_price=200.0)
        offer = ContractTerms(price=50.0)  # Well below acceptable
        decision = s.evaluate_offer(offer, MarketContext(), 1)
        assert decision["action"] == "counter"
        assert decision["counter_offer"].price > 50.0


class TestConcessionStrategy:
    def test_initial_offer(self) -> None:
        s = ConcessionStrategy(reservation_price=40.0)
        offer = s.generate_initial_offer(MarketContext())
        assert offer.price == 72.0  # 40 * 1.8

    def test_concedes_over_rounds(self) -> None:
        s = ConcessionStrategy(reservation_price=40.0, opening_price=100.0)

        # Round 1: target ~100 - 5.5 = 94.5
        decision1 = s.evaluate_offer(ContractTerms(price=50.0), MarketContext(), 1)
        assert decision1["action"] == "counter"
        # Round 1 target: 100 - (10*1*0.55) = 100 - 5.5 = 94.5
        assert decision1["counter_offer"].price > 50.0

        # Round 5: target lower
        decision5 = s.evaluate_offer(ContractTerms(price=50.0), MarketContext(), 5)
        assert decision5["action"] == "counter"
        # Round 5 target should be lower than round 1
        assert decision5["counter_offer"].price < decision1["counter_offer"].price

    def test_accepts_when_offer_above_target(self) -> None:
        s = ConcessionStrategy(reservation_price=40.0, opening_price=100.0)
        # In round 1, target is high, so 120 exceeds it
        decision = s.evaluate_offer(ContractTerms(price=120.0), MarketContext(), 1)
        assert decision["action"] == "accept"


class TestBATNAStrategy:
    def test_initial_offer(self) -> None:
        s = BATNAStrategy(batna_value=50.0)
        offer = s.generate_initial_offer(MarketContext())
        assert offer.price == 97.5  # target(65) * 1.5

    def test_accept_above_target(self) -> None:
        s = BATNAStrategy(batna_value=50.0, target_price=80.0)
        decision = s.evaluate_offer(ContractTerms(price=90.0), MarketContext(), 1)
        assert decision["action"] == "accept"

    def test_withdraw_below_batna(self) -> None:
        s = BATNAStrategy(batna_value=100.0)
        decision = s.evaluate_offer(ContractTerms(price=20.0), MarketContext(), 1)
        assert decision["action"] == "withdraw"

    def test_counter_between(self) -> None:
        s = BATNAStrategy(batna_value=50.0, target_price=100.0)
        decision = s.evaluate_offer(ContractTerms(price=60.0), MarketContext(), 1)
        assert decision["action"] == "counter"
        # Counter should be midpoint of 60 and 100 = 80
        assert 70 <= decision["counter_offer"].price <= 90


class TestValueBasedStrategy:
    def test_initial_offer_with_reputation(self) -> None:
        s = ValueBasedStrategy(base_price=100.0, value_multiplier=1.5)
        ctx = MarketContext(counterparty_reputation=90.0)
        offer = s.generate_initial_offer(ctx)
        # price = 100 * 1.5 * (1 + 0.9 * 0.2) = 100 * 1.5 * 1.18 = 177
        assert offer.price > 150.0

    def test_accept_above_value_adjusted(self) -> None:
        s = ValueBasedStrategy(base_price=100.0, min_acceptable=60.0)
        decision = s.evaluate_offer(ContractTerms(price=120.0), MarketContext(), 1)
        assert decision["action"] == "accept"

    def test_reject_below_minimum(self) -> None:
        s = ValueBasedStrategy(base_price=100.0, min_acceptable=70.0)
        decision = s.evaluate_offer(ContractTerms(price=50.0), MarketContext(), 1)
        assert decision["action"] == "reject"


class TestStrategyFactory:
    def test_create_known_strategies(self) -> None:
        kwargs_map = {
            "tit-for-tat": {"reservation_price": 100.0},
            "concession": {"reservation_price": 100.0},
            "batna": {"batna_value": 100.0, "target_price": 130.0},
            "value-based": {"base_price": 100.0},
        }
        for name, kwargs in kwargs_map.items():
            s = create_strategy(name, **kwargs)
            assert s.name == name

    def test_create_unknown_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown strategy"):
            create_strategy("nonexistent", reservation_price=100.0)


class TestNegotiationEngine:
    @pytest.fixture
    def engine(self) -> NegotiationEngine:
        return NegotiationEngine()

    def test_start_session(self, engine: NegotiationEngine) -> None:
        session = engine.start_session("buyer-1", "seller-1", "purchase")
        assert session.buyer_id == "buyer-1"
        assert session.seller_id == "seller-1"
        assert engine.active_sessions == 1

    def test_get_close_session(self, engine: NegotiationEngine) -> None:
        session = engine.start_session("b", "s")
        assert engine.get_session(session.session_id) is not None
        engine.close_session(session.session_id)
        assert engine.get_session(session.session_id) is None

    @pytest.mark.asyncio
    async def test_negotiate_agreement(self, engine: NegotiationEngine) -> None:
        """Buyer and seller with overlapping ranges should agree."""
        session = engine.start_session("buyer", "seller", "purchase", max_rounds=5)

        buyer = ConcessionStrategy(reservation_price=80.0, opening_price=50.0)
        seller = ConcessionStrategy(reservation_price=40.0, opening_price=100.0)

        outcome = await engine.negotiate(session, buyer, seller)

        assert outcome.outcome_type == OutcomeType.AGREEMENT
        assert outcome.agreed_terms is not None
        assert 40.0 <= outcome.agreed_terms.price <= 100.0

    @pytest.mark.asyncio
    async def test_negotiate_deadlock(self, engine: NegotiationEngine) -> None:
        """Buyer and seller with non-overlapping ranges should deadlock."""
        session = engine.start_session("buyer", "seller", "purchase", max_rounds=3)

        # Buyer won't pay more than 30, seller won't accept less than 70
        buyer = BATNAStrategy(batna_value=50.0, target_price=30.0)
        seller = BATNAStrategy(batna_value=100.0, target_price=70.0)

        outcome = await engine.negotiate(session, buyer, seller)

        assert outcome.outcome_type in (
            OutcomeType.DEADLOCK,
            OutcomeType.WITHDRAWAL,
            OutcomeType.MAX_ROUNDS,
        )

    @pytest.mark.asyncio
    async def test_negotiate_buyer_withdraws(self, engine: NegotiationEngine) -> None:
        session = engine.start_session("buyer", "seller", "purchase", max_rounds=5)

        # Buyer with very weak BATNA will withdraw if offer is bad
        buyer = BATNAStrategy(batna_value=80.0, target_price=60.0)
        seller = ConcessionStrategy(reservation_price=100.0, opening_price=200.0)

        outcome = await engine.negotiate(session, buyer, seller)

        # With seller's high prices, buyer should either withdraw or deadlock
        assert outcome.agreed_terms is None  # No agreement

    def test_deadlock_detection_no_movement(self, engine: NegotiationEngine) -> None:
        session = engine.start_session("b", "s", max_rounds=10)

        # Add 3 rounds with no price movement
        for i in range(3):
            from acp.protocol.models import NegotiationRound
            terms = ContractTerms(price=100.0)
            session.rounds.append(NegotiationRound(
                round_number=i + 1, offer=terms,
                rationale="", strategy_used="test",
            ))

        assert engine.detect_deadlock(session, consecutive_stall_rounds=3) is True

    def test_deadlock_detection_enough_movement(self, engine: NegotiationEngine) -> None:
        session = engine.start_session("b", "s", max_rounds=10)

        from acp.protocol.models import NegotiationRound
        # Add 3 rounds with price movement
        session.rounds.append(NegotiationRound(
            round_number=1, offer=ContractTerms(price=100.0),
            rationale="", strategy_used="test",
        ))
        session.rounds.append(NegotiationRound(
            round_number=2, offer=ContractTerms(price=90.0),
            rationale="", strategy_used="test",
        ))
        session.rounds.append(NegotiationRound(
            round_number=3, offer=ContractTerms(price=85.0),
            rationale="", strategy_used="test",
        ))

        assert engine.detect_deadlock(session, consecutive_stall_rounds=3) is False
