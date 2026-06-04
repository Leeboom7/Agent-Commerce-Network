"""
ACP Reputation System — Ratings & Scoring.

Multi-layer reputation for the Agent Commerce Network:
1. Direct ratings per transaction
2. Time-weighted composite score (recent ratings matter more)
3. Success rate tracking
"""

from __future__ import annotations

import math
from datetime import UTC, datetime

from acp.protocol.models import Rating, ReputationRecord


class ReputationEngine:
    """
    Manages agent reputation across the commerce network.

    Reputation is computed from:
    - Direct transaction ratings (quality, timeliness, communication, accuracy)
    - Time-weighted decay (90-day half-life by default)
    - Success/failure ratio
    - Total transaction volume
    """

    def __init__(self, half_life_days: float = 90.0) -> None:
        self.half_life_days = half_life_days
        self._records: dict[str, ReputationRecord] = {}

    # ── Rating Submission ──────────────────────────────────

    def submit_rating(self, rating: Rating) -> None:
        """
        Submit a rating for a transaction.

        The rating is for the counterparty. The rater_id is the agent
        submitting the rating; the rated agent's record is updated.
        """
        # Determine who is being rated (the counterparty in the transaction)
        rated_id = self._get_rated_agent(rating)
        if rated_id is None:
            return

        record = self._get_or_create_record(rated_id)
        record.ratings.append(rating)
        record.total_transactions += 1

        if rating.overall >= 3.0:
            record.successful_transactions += 1

        # Recalculate composite
        record.composite_score = self._compute_composite(record)

    def submit_rating_direct(
        self, rated_agent_id: str, rater_id: str,
        transaction_id: str, scores: dict[str, float],
        comment: str = "",
    ) -> Rating:
        """
        Submit a rating directly by agent IDs.
        Convenience method.
        """
        rating = Rating(
            rater_id=rater_id,
            transaction_id=transaction_id,
            scores=scores,
            comment=comment,
        )
        # Manually set the rated agent
        record = self._get_or_create_record(rated_agent_id)
        record.ratings.append(rating)
        record.total_transactions += 1

        if rating.overall >= 3.0:
            record.successful_transactions += 1

        record.composite_score = self._compute_composite(record)
        return rating

    # ── Query ─────────────────────────────────────────────

    def get_reputation(self, agent_id: str) -> ReputationRecord:
        """Get an agent's reputation record."""
        return self._get_or_create_record(agent_id)

    def get_score(self, agent_id: str) -> float:
        """Get just the composite score (0-100)."""
        return self._get_or_create_record(agent_id).composite_score

    def get_top_agents(
        self, min_transactions: int = 1, limit: int = 10
    ) -> list[tuple[str, float]]:
        """Get agents ranked by reputation score."""
        candidates = [
            (aid, rec.composite_score)
            for aid, rec in self._records.items()
            if rec.total_transactions >= min_transactions
        ]
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:limit]

    # ── Core Computation ──────────────────────────────────

    def _compute_composite(self, record: ReputationRecord) -> float:
        """
        Compute the time-weighted composite reputation score.

        Formula:
            composite = Σ(rating × e^(-λ × age)) / Σ(e^(-λ × age))

        where λ = ln(2) / half_life_days
        """
        if not record.ratings:
            return 100.0  # Neutral starting score

        decay = math.log(2) / self.half_life_days
        now = datetime.now(UTC)

        weighted_sum = 0.0
        weight_sum = 0.0

        for rating in record.ratings:
            age_days = (now - rating.timestamp).total_seconds() / 86400.0
            weight = math.exp(-decay * age_days)
            weighted_sum += rating.overall * weight
            weight_sum += weight

        if weight_sum == 0:
            return 100.0

        # Scale from 5-point to 100-point
        raw = (weighted_sum / weight_sum) * 20.0

        # Blend with success rate for stability
        success_bonus = record.success_rate * 10.0  # Up to 10 points bonus

        # Volume adjustment: new agents with few ratings regress to mean
        if record.total_transactions < 5:
            volume_factor = record.total_transactions / 5.0
            raw = raw * volume_factor + 50.0 * (1 - volume_factor)

        return round(min(100.0, max(0.0, raw + success_bonus)), 1)

    # ── Helpers ───────────────────────────────────────────

    def _get_or_create_record(self, agent_id: str) -> ReputationRecord:
        if agent_id not in self._records:
            self._records[agent_id] = ReputationRecord(agent_id=agent_id)
        return self._records[agent_id]

    def _get_rated_agent(self, rating: Rating) -> str | None:
        """Infer which agent is being rated."""
        # In practice, the rated agent is derived from the transaction context.
        # For now, we assume the rated agent ID is stored in the rating or
        # derivable from the transaction. This is a simplification.
        # The direct method submit_rating_direct() should be preferred.
        return None  # Subclasses/overrides should handle this

    @property
    def total_agents(self) -> int:
        return len(self._records)
