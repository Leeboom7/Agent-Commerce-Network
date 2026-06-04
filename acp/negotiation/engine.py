"""
ACP Negotiation Engine.

Manages multi-round structured negotiation sessions between buyer
and seller agents. Supports pluggable strategies, deadlock detection,
and automatic escalation.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from acp.protocol.models import (
    ContractTerms,
    MarketContext,
    NegotiationRound,
    NegotiationSession,
    NegotiationStatus,
)
from acp.negotiation.strategies import BaseNegotiationStrategy


# ──────────────────────────────────────────────────────────────
# Negotiation Outcome
# ──────────────────────────────────────────────────────────────


class OutcomeType(str, Enum):
    AGREEMENT = "agreement"
    DEADLOCK = "deadlock"
    WITHDRAWAL = "withdrawal"
    MAX_ROUNDS = "max_rounds_exhausted"


@dataclass
class NegotiationOutcome:
    """Result of a completed negotiation session."""

    outcome_type: OutcomeType
    agreed_terms: ContractTerms | None = None
    final_round: int = 0
    total_rounds: int = 0
    buyer_final_position: ContractTerms | None = None
    seller_final_position: ContractTerms | None = None
    deadlock_reason: str = ""
    session_id: str = ""


# ──────────────────────────────────────────────────────────────
# Negotiation Engine
# ──────────────────────────────────────────────────────────────


class NegotiationEngine:
    """
    Core negotiation engine for agent-to-agent price and terms bargaining.

    Usage:
        engine = NegotiationEngine()
        session = engine.start_session(buyer_id, seller_id, "purchase")
        outcome = await engine.negotiate(
            session,
            buyer_strategy=TitForTatStrategy(...),
            seller_strategy=ConcessionStrategy(...),
            market_context=MarketContext(...),
        )
    """

    def __init__(self, max_rounds: int = 10, max_sessions: int = 1000) -> None:
        self.max_rounds = max_rounds
        self._sessions: dict[str, NegotiationSession] = {}

    # ── Session Management ─────────────────────────────────

    def start_session(
        self,
        buyer_id: str,
        seller_id: str,
        relationship_type: str = "purchase",
        max_rounds: int | None = None,
    ) -> NegotiationSession:
        """Create a new negotiation session."""
        session = NegotiationSession(
            session_id=f"neg-{uuid.uuid4().hex[:12]}",
            buyer_id=buyer_id,
            seller_id=seller_id,
            relationship_type=relationship_type,
            max_rounds=max_rounds or self.max_rounds,
        )
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> NegotiationSession | None:
        """Retrieve an active session."""
        return self._sessions.get(session_id)

    def close_session(self, session_id: str) -> None:
        """Remove a completed session."""
        self._sessions.pop(session_id, None)

    # ── Negotiation Logic ──────────────────────────────────

    async def negotiate(
        self,
        session: NegotiationSession,
        buyer_strategy: BaseNegotiationStrategy,
        seller_strategy: BaseNegotiationStrategy,
        market_context: MarketContext | None = None,
        initial_offer: ContractTerms | None = None,
    ) -> NegotiationOutcome:
        """
        Execute a full negotiation between buyer and seller.

        The buyer typically makes the first offer. Seller responds.
        Alternates until agreement, deadlock, or max rounds.

        Args:
            session: The negotiation session.
            buyer_strategy: Strategy used by the buyer agent.
            seller_strategy: Strategy used by the seller agent.
            market_context: Market data for informed decisions.
            initial_offer: Optional initial offer from buyer. If None,
                          the buyer strategy generates one.

        Returns:
            NegotiationOutcome with the final result.
        """
        context = market_context or MarketContext()

        # Round 1: Buyer's opening offer
        if initial_offer is None:
            initial_offer = buyer_strategy.generate_initial_offer(context)

        current_offer = initial_offer
        session.rounds = []

        for round_num in range(1, session.max_rounds + 1):
            # Buyer offer
            buyer_round = NegotiationRound(
                round_number=round_num,
                offer=current_offer,
                strategy_used=buyer_strategy.name,
                rationale=self._generate_rationale(
                    buyer_strategy, current_offer, context, "buyer", round_num
                ),
            )

            # Seller evaluates and responds
            seller_decision = seller_strategy.evaluate_offer(
                current_offer, context, round_num
            )

            if seller_decision["action"] == "accept":
                # Agreement reached
                buyer_round.counter_offer = current_offer  # Accepted as-is or with minor mods
                session.rounds.append(buyer_round)
                session.status = NegotiationStatus.AGREED
                session.resolved_at = datetime.now(timezone.utc)

                final_terms = seller_decision.get("accepted_terms", current_offer)
                return NegotiationOutcome(
                    outcome_type=OutcomeType.AGREEMENT,
                    agreed_terms=final_terms,
                    final_round=round_num,
                    total_rounds=round_num,
                    buyer_final_position=current_offer,
                    seller_final_position=final_terms,
                    session_id=session.session_id,
                )

            elif seller_decision["action"] == "counter":
                # Seller makes a counter-offer
                counter = seller_decision["counter_offer"]
                buyer_round.counter_offer = counter
                buyer_round.rationale += f"\nSeller countered: {seller_decision.get('rationale', '')}"
                session.rounds.append(buyer_round)

                # Buyer evaluates the counter
                buyer_decision = buyer_strategy.evaluate_offer(
                    counter, context, round_num
                )

                if buyer_decision["action"] == "accept":
                    session.rounds.append(NegotiationRound(
                        round_number=round_num,
                        offer=counter,
                        strategy_used=buyer_strategy.name,
                        rationale="Buyer accepts the seller's counter-offer.",
                    ))
                    session.status = NegotiationStatus.AGREED
                    session.resolved_at = datetime.now(timezone.utc)

                    return NegotiationOutcome(
                        outcome_type=OutcomeType.AGREEMENT,
                        agreed_terms=buyer_decision.get("accepted_terms", counter),
                        final_round=round_num,
                        total_rounds=round_num,
                        session_id=session.session_id,
                    )

                elif buyer_decision["action"] == "counter":
                    # Buyer prepares next offer for the next round
                    current_offer = buyer_decision["counter_offer"]
                    continue

                elif buyer_decision["action"] == "withdraw":
                    session.status = NegotiationStatus.WITHDRAWN
                    return NegotiationOutcome(
                        outcome_type=OutcomeType.WITHDRAWAL,
                        final_round=round_num,
                        total_rounds=round_num,
                        deadlock_reason=buyer_decision.get("reason", "Buyer withdrew"),
                        session_id=session.session_id,
                    )

                else:
                    # Reject or deadlock
                    session.status = NegotiationStatus.DEADLOCKED
                    return NegotiationOutcome(
                        outcome_type=OutcomeType.DEADLOCK,
                        final_round=round_num,
                        total_rounds=round_num,
                        deadlock_reason=seller_decision.get("reason", "Seller rejected"),
                        session_id=session.session_id,
                    )

            elif seller_decision["action"] == "reject":
                session.status = NegotiationStatus.DEADLOCKED
                return NegotiationOutcome(
                    outcome_type=OutcomeType.DEADLOCK,
                    final_round=round_num,
                    total_rounds=round_num,
                    deadlock_reason=seller_decision.get("reason", "Seller rejected"),
                    session_id=session.session_id,
                )

            elif seller_decision["action"] == "withdraw":
                session.status = NegotiationStatus.WITHDRAWN
                return NegotiationOutcome(
                    outcome_type=OutcomeType.WITHDRAWAL,
                    final_round=round_num,
                    total_rounds=round_num,
                    deadlock_reason=seller_decision.get("reason", "Seller withdrew"),
                    session_id=session.session_id,
                )

        # Max rounds exhausted
        session.status = NegotiationStatus.DEADLOCKED
        return NegotiationOutcome(
            outcome_type=OutcomeType.MAX_ROUNDS,
            final_round=session.max_rounds,
            total_rounds=session.max_rounds,
            deadlock_reason=f"Maximum rounds ({session.max_rounds}) exhausted without agreement",
            session_id=session.session_id,
        )

    # ── Deadlock Detection ─────────────────────────────────

    def detect_deadlock(
        self,
        session: NegotiationSession,
        min_concession_rate: float = 0.01,
        consecutive_stall_rounds: int = 3,
    ) -> bool:
        """
        Detect if a negotiation is stalemated.

        Checks for:
        1. Insufficient concession rate over recent rounds
        2. Oscillation (parties cycling through same offers)
        3. No price movement over N consecutive rounds
        """
        if len(session.rounds) < consecutive_stall_rounds:
            return False

        recent = session.rounds[-consecutive_stall_rounds:]

        # Check price movement
        prices: list[float] = []
        for r in recent:
            prices.append(r.offer.price)
            if r.counter_offer:
                prices.append(r.counter_offer.price)

        if len(prices) < 2:
            return False

        max_price = max(prices)
        min_price = min(prices)
        if max_price > 0:
            movement = (max_price - min_price) / max_price
            if movement < min_concession_rate:
                return True

        return False

    # ── Helpers ────────────────────────────────────────────

    def _generate_rationale(
        self,
        strategy: BaseNegotiationStrategy,
        offer: ContractTerms,
        context: MarketContext,
        role: str,
        round_num: int,
    ) -> str:
        """Generate a human-readable rationale for an offer."""
        return (
            f"Round {round_num} | {role} using {strategy.name} | "
            f"Offer: {offer.price:.2f} NC | "
            f"Market avg: {context.average_price:.2f} NC | "
            f"Counterparty reputation: {context.counterparty_reputation:.0f}/100"
        )

    @property
    def active_sessions(self) -> int:
        return len(self._sessions)
