"""
ACP Negotiation Strategies.

Pluggable strategies that agents use during multi-round negotiation.
Each strategy implements the same interface, allowing agents to
switch strategies based on context (market conditions, counterparty,
transaction type).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any

from acp.protocol.models import ContractTerms, MarketContext


# ──────────────────────────────────────────────────────────────
# Base Strategy Interface
# ──────────────────────────────────────────────────────────────


class BaseNegotiationStrategy(ABC):
    """
    Abstract base for all negotiation strategies.

    Strategies are stateless per session — the NegotiationEngine
    manages session state. Strategies provide decision logic only.
    """

    name: str = "base"

    @abstractmethod
    def generate_initial_offer(self, context: MarketContext) -> ContractTerms:
        """Generate the opening offer."""
        ...

    @abstractmethod
    def evaluate_offer(
        self,
        offer: ContractTerms,
        context: MarketContext,
        round_num: int,
    ) -> dict[str, Any]:
        """
        Evaluate an incoming offer and decide: accept, counter, reject, or withdraw.

        Returns a dict with:
        - action: "accept" | "counter" | "reject" | "withdraw"
        - counter_offer: ContractTerms (if action is "counter")
        - accepted_terms: ContractTerms (if action is "accept", may be same as offer)
        - reason: str (explanation for reject/withdraw)
        - rationale: str (explanation for any action)
        """
        ...

    def calculate_utility(self, terms: ContractTerms, context: MarketContext) -> float:
        """
        Calculate the utility of a given offer for this strategy.
        Higher = better. Used internally for decision-making.
        """
        # Default: utility = 1 / price (simpler preferred)
        if terms.price <= 0:
            return float("inf")
        return 1.0 / terms.price


# ──────────────────────────────────────────────────────────────
# Strategy 1: Tit-for-Tat
# ──────────────────────────────────────────────────────────────


class TitForTatStrategy(BaseNegotiationStrategy):
    """
    Tit-for-Tat negotiation strategy.

    Starts cooperative. Mirrors the counterparty's behavior:
    - If they concede, we concede proportionally.
    - If they stall, we stall.
    - If they make a reasonable offer, we accept.

    Best for: repeated interactions, reputation-sensitive markets.
    """

    name = "tit-for-tat"

    def __init__(
        self,
        reservation_price: float,
        opening_price: float | None = None,
        concession_rate: float = 0.05,  # Fraction conceded per round
        max_rounds: int = 10,
    ) -> None:
        self.reservation_price = reservation_price
        self.opening_price = opening_price or reservation_price * 1.5
        self.concession_rate = concession_rate
        self.max_rounds = max_rounds
        self._last_counterparty_concession: float | None = None

    def generate_initial_offer(self, context: MarketContext) -> ContractTerms:
        price = self.opening_price
        if context.average_price > 0:
            # Anchor to market average if available
            price = context.average_price * 1.2
        return ContractTerms(
            price=round(price, 2),
            deadline="2026-07-15T00:00:00Z",
            revision_rounds=2,
            penalty_rate=0.10,
        )

    def evaluate_offer(
        self, offer: ContractTerms, context: MarketContext, round_num: int
    ) -> dict[str, Any]:
        # Calculate the gap
        if offer.price >= self.reservation_price * 0.9:
            # Offer is acceptable
            self._last_counterparty_concession = None
            return {
                "action": "accept",
                "accepted_terms": offer,
                "rationale": f"Offer of {offer.price:.2f} meets or exceeds reservation threshold.",
            }

        # Calculate concession from counterparty
        if self._last_counterparty_concession is not None:
            counterparty_conceded = offer.price > self._last_counterparty_concession
        else:
            counterparty_conceded = True  # First round, assume good faith

        # Mirror behavior
        if counterparty_conceded:
            # Concede proportionally
            new_price = offer.price * (1 + self.concession_rate)
            new_price = min(new_price, self.opening_price)  # Don't exceed opening
            self._last_counterparty_concession = new_price

            return {
                "action": "counter",
                "counter_offer": ContractTerms(
                    price=round(new_price, 2),
                    deadline=offer.deadline,
                    revision_rounds=offer.revision_rounds,
                    penalty_rate=offer.penalty_rate,
                ),
                "rationale": f"Reciprocal concession: countering at {new_price:.2f} NC.",
            }
        else:
            # Counterparty stalled — hold firm
            remaining = self.max_rounds - round_num
            if remaining <= 1:
                # Last round — accept if above reservation
                if offer.price >= self.reservation_price:
                    return {
                        "action": "accept",
                        "accepted_terms": offer,
                        "rationale": "Final round: accepting best available offer.",
                    }

            return {
                "action": "reject",
                "reason": "Counterparty is not conceding. Holding position.",
                "rationale": "No concession detected; maintaining current position.",
            }


# ──────────────────────────────────────────────────────────────
# Strategy 2: Concession-Based
# ──────────────────────────────────────────────────────────────


class ConcessionStrategy(BaseNegotiationStrategy):
    """
    Gradual concession strategy.

    Starts high, concedes predictably each round toward the reservation
    price. The concession schedule is linear by default.

    Best for: one-shot transactions where reputation matters less.
    Most realistic for automated agent negotiation in thin markets.
    """

    name = "concession"

    def __init__(
        self,
        reservation_price: float,
        opening_price: float | None = None,
        concession_per_round: float | None = None,
        max_rounds: int = 10,
        firmness: float = 0.5,  # 0=very yielding, 1=very firm
    ) -> None:
        self.reservation_price = reservation_price
        self.opening_price = opening_price or reservation_price * 1.8
        self.max_rounds = max_rounds
        self.firmness = firmness

        # Calculate fixed concession per round
        total_concession = self.opening_price - reservation_price
        if concession_per_round is not None:
            self.concession_per_round = concession_per_round
        else:
            self.concession_per_round = total_concession / max_rounds

    def generate_initial_offer(self, context: MarketContext) -> ContractTerms:
        price = self.opening_price
        if context.average_price > 0:
            price = max(price, context.average_price * 1.3)
        return ContractTerms(
            price=round(price, 2),
            deadline="2026-07-15T00:00:00Z",
            revision_rounds=2,
            penalty_rate=0.10,
        )

    def evaluate_offer(
        self, offer: ContractTerms, context: MarketContext, round_num: int
    ) -> dict[str, Any]:
        # Calculate my target price for this round
        conceded = self.concession_per_round * round_num * (1 - self.firmness + 0.05)
        my_target = self.opening_price - conceded
        my_target = max(my_target, self.reservation_price)

        # Accept if offer exceeds my target
        if offer.price >= my_target:
            return {
                "action": "accept",
                "accepted_terms": offer,
                "rationale": (
                    f"Offer ({offer.price:.2f}) meets round-{round_num} target "
                    f"({my_target:.2f}). Accepting."
                ),
            }

        # Counter at my target
        return {
            "action": "counter",
            "counter_offer": ContractTerms(
                price=round(my_target, 2),
                deadline=offer.deadline,
                revision_rounds=offer.revision_rounds,
                penalty_rate=offer.penalty_rate,
            ),
            "rationale": (
                f"Countering at round-{round_num} target price: {my_target:.2f} NC "
                f"(reservation: {self.reservation_price:.2f})."
            ),
        }


# ──────────────────────────────────────────────────────────────
# Strategy 3: BATNA-Driven
# ──────────────────────────────────────────────────────────────


class BATNAStrategy(BaseNegotiationStrategy):
    """
    Best Alternative To a Negotiated Agreement strategy.

    Calculates a precise walk-away point based on the BATNA value.
    If the offer is worse than BATNA, reject. If better, accept or
    counter near the BATNA-adjusted threshold.

    Best for: markets with many alternatives, price-sensitive agents.
    """

    name = "batna"

    def __init__(
        self,
        batna_value: float,  # Value of the best alternative if no deal
        target_price: float | None = None,
        opening_price: float | None = None,
        negotiation_cost_per_round: float = 1.0,  # Cost of each negotiation round
    ) -> None:
        self.batna_value = batna_value
        self.target_price = target_price or batna_value * 1.3
        self.opening_price = opening_price or self.target_price * 1.5
        self.negotiation_cost_per_round = negotiation_cost_per_round

    def generate_initial_offer(self, context: MarketContext) -> ContractTerms:
        return ContractTerms(
            price=round(self.opening_price, 2),
            deadline="2026-07-15T00:00:00Z",
            revision_rounds=2,
            penalty_rate=0.10,
        )

    def evaluate_offer(
        self, offer: ContractTerms, context: MarketContext, round_num: int
    ) -> dict[str, Any]:
        # BATNA minus accumulated negotiation costs
        effective_batna = self.batna_value - (self.negotiation_cost_per_round * round_num)

        if offer.price >= self.target_price:
            return {
                "action": "accept",
                "accepted_terms": offer,
                "rationale": (
                    f"Offer ({offer.price:.2f}) exceeds target ({self.target_price:.2f}). Accepting."
                ),
            }

        if offer.price < effective_batna:
            # Worse than walking away
            return {
                "action": "withdraw",
                "reason": (
                    f"Offer ({offer.price:.2f}) below effective BATNA "
                    f"({effective_batna:.2f}). Walking away."
                ),
                "rationale": "Better alternatives exist; withdrawing from negotiation.",
            }

        # Counter between offer and target
        counter_price = (offer.price + self.target_price) / 2
        return {
            "action": "counter",
            "counter_offer": ContractTerms(
                price=round(counter_price, 2),
                deadline=offer.deadline,
                revision_rounds=offer.revision_rounds,
                penalty_rate=offer.penalty_rate,
            ),
            "rationale": (
                f"BATNA: {self.batna_value:.2f}, Target: {self.target_price:.2f}. "
                f"Countering at midpoint: {counter_price:.2f}."
            ),
        }


# ──────────────────────────────────────────────────────────────
# Strategy 4: Value-Based
# ──────────────────────────────────────────────────────────────


class ValueBasedStrategy(BaseNegotiationStrategy):
    """
    Value-based negotiation strategy.

    Prices based on the estimated value delivered, using market
    comparables and counterparty reputation to adjust.

    Best for: premium services, quality-sensitive markets.
    """

    name = "value-based"

    def __init__(
        self,
        base_price: float,
        value_multiplier: float = 1.0,  # Premium for quality/reputation
        min_acceptable: float | None = None,
        reputation_weight: float = 0.2,  # How much reputation affects price
    ) -> None:
        self.base_price = base_price
        self.value_multiplier = value_multiplier
        self.min_acceptable = min_acceptable or base_price * 0.7
        self.reputation_weight = reputation_weight

    def generate_initial_offer(self, context: MarketContext) -> ContractTerms:
        # Premium pricing based on counterparty quality
        reputation_premium = 1 + (
            (context.counterparty_reputation / 100.0) * self.reputation_weight
        )
        market_adj = 1.0
        if context.average_price > 0:
            market_adj = context.average_price / self.base_price

        price = self.base_price * self.value_multiplier * reputation_premium * market_adj

        return ContractTerms(
            price=round(price, 2),
            deadline="2026-07-15T00:00:00Z",
            revision_rounds=2,
            penalty_rate=0.10,
        )

    def evaluate_offer(
        self, offer: ContractTerms, context: MarketContext, round_num: int
    ) -> dict[str, Any]:
        # Calculate value-adjusted acceptable price
        reputation_discount = 1 - (
            (100 - context.counterparty_reputation) / 100.0 * self.reputation_weight
        )
        acceptable = self.base_price * reputation_discount
        acceptable = max(acceptable, self.min_acceptable)

        if offer.price >= acceptable:
            return {
                "action": "accept",
                "accepted_terms": offer,
                "rationale": (
                    f"Offer ({offer.price:.2f}) meets value-adjusted threshold "
                    f"({acceptable:.2f}). Accepting."
                ),
            }

        if offer.price < self.min_acceptable:
            return {
                "action": "reject",
                "reason": f"Offer ({offer.price:.2f}) below minimum acceptable ({self.min_acceptable:.2f}).",
                "rationale": "Cannot deliver quality below minimum price point.",
            }

        # Counter at value-based price
        counter_price = (offer.price + acceptable) / 2
        return {
            "action": "counter",
            "counter_offer": ContractTerms(
                price=round(counter_price, 2),
                deadline=offer.deadline,
                revision_rounds=offer.revision_rounds,
                penalty_rate=offer.penalty_rate,
            ),
            "rationale": (
                f"Base: {self.base_price:.2f}, Value-adj: {acceptable:.2f}. "
                f"Countering: {counter_price:.2f}."
            ),
        }


# ──────────────────────────────────────────────────────────────
# Strategy Factory
# ──────────────────────────────────────────────────────────────


def create_strategy(
    strategy_type: str,
    **kwargs: Any,
) -> BaseNegotiationStrategy:
    """
    Factory for creating negotiation strategies.

    Args:
        strategy_type: "tit-for-tat", "concession", "batna", or "value-based"
        **kwargs: Strategy-specific parameters.

    Returns:
        Configured strategy instance.
    """
    strategies: dict[str, type[BaseNegotiationStrategy]] = {
        "tit-for-tat": TitForTatStrategy,
        "concession": ConcessionStrategy,
        "batna": BATNAStrategy,
        "value-based": ValueBasedStrategy,
    }

    strategy_class = strategies.get(strategy_type)
    if strategy_class is None:
        raise ValueError(
            f"Unknown strategy: {strategy_type}. "
            f"Available: {list(strategies.keys())}"
        )

    return strategy_class(**kwargs)
