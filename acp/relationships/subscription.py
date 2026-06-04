"""
ACP Relationship: Subscription.

Subscribe to an agent's ongoing capability. The subscriber pays a
recurring fee (per period) for continuous access to a service.

Example: Orchestrator subscribes to a monitoring agent that continuously
watches system metrics and alerts on anomalies. Billed monthly.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from acp.contract.manager import ContractManager
from acp.negotiation.engine import NegotiationEngine
from acp.negotiation.strategies import BaseNegotiationStrategy, create_strategy
from acp.protocol.models import (
    ContractTerms,
    MarketContext,
    ServiceContract,
)


class SubscriptionRelationship:
    """
    Implements the 'subscription' economic relationship type.

    Flow:
    1. Subscriber discovers a service with subscription pricing
    2. Subscriber and provider negotiate subscription terms
    3. Contract is created with renewal terms
    4. Provider delivers ongoing service
    5. Subscriber pays periodically (auto-charged)
    6. Either party can cancel with notice
    """

    def __init__(
        self,
        engine: NegotiationEngine | None = None,
        contract_mgr: ContractManager | None = None,
    ) -> None:
        self.engine = engine or NegotiationEngine()
        self.contract_mgr = contract_mgr or ContractManager()
        self._active_subscriptions: dict[str, dict[str, Any]] = {}

    async def subscribe(
        self,
        subscriber_id: str,
        provider_id: str,
        service_description: str,
        period: str = "monthly",  # daily, weekly, monthly
        max_periods: int = 12,
        subscriber_strategy: BaseNegotiationStrategy | None = None,
        provider_strategy: BaseNegotiationStrategy | None = None,
        market_context: MarketContext | None = None,
    ) -> dict:
        """
        Set up a subscription relationship.

        Args:
            subscriber_id: Agent subscribing to the service.
            provider_id: Agent providing the ongoing service.
            service_description: What the provider will do continuously.
            period: Billing period ("daily", "weekly", "monthly").
            max_periods: Maximum number of periods (0 = indefinite).
            subscriber_strategy: Negotiation strategy for subscriber.
            provider_strategy: Negotiation strategy for provider.
            market_context: Market data.

        Returns:
            dict with success, contract, details.
        """
        context = market_context or MarketContext()

        # Subscriptions typically have lower per-period pricing
        monthly_estimate = context.average_price or 50.0

        if subscriber_strategy is None:
            subscriber_strategy = create_strategy(
                "tit-for-tat",
                reservation_price=monthly_estimate * 2.0,
                opening_price=monthly_estimate * 0.5,
            )
        if provider_strategy is None:
            provider_strategy = create_strategy(
                "value-based",
                base_price=monthly_estimate,
                value_multiplier=1.3,
            )

        # Negotiate
        session = self.engine.start_session(
            subscriber_id, provider_id, "subscription"
        )
        outcome = await self.engine.negotiate(
            session, subscriber_strategy, provider_strategy, context,
        )

        if outcome.agreed_terms is None:
            self.engine.close_session(session.session_id)
            return {
                "success": False,
                "contract": None,
                "details": f"Subscription negotiation failed: {outcome.outcome_type.value}",
            }

        # Embed subscription metadata
        terms = outcome.agreed_terms
        terms.metadata["subscription"] = {
            "service": service_description,
            "period": period,
            "price_per_period": terms.price,
            "max_periods": max_periods,
            "periods_paid": 0,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }

        # Create contract
        contract = self.contract_mgr.create_contract(
            buyer_id=subscriber_id,
            seller_id=provider_id,
            relationship_type="subscription",
            terms=terms,
            negotiation_session_id=session.session_id,
        )
        self.contract_mgr.sign(contract.contract_id, subscriber_id)
        self.contract_mgr.sign(contract.contract_id, provider_id)

        self._active_subscriptions[contract.contract_id] = {
            "subscriber": subscriber_id,
            "provider": provider_id,
            "period": period,
            "price": terms.price,
            "periods_paid": 0,
            "max_periods": max_periods,
            "status": "active",
        }

        self.engine.close_session(session.session_id)

        return {
            "success": True,
            "contract": contract,
            "details": (
                f"Subscription: {subscriber_id} subscribes to {provider_id} "
                f"for {service_description} at {terms.price} NC/{period}. "
                f"Contract: {contract.contract_id}"
            ),
        }

    def process_periodic_payment(
        self, contract_id: str, ledger: Any,
    ) -> dict:
        """
        Process a periodic subscription payment.
        Called by a scheduler or orchestrator.
        """
        sub = self._active_subscriptions.get(contract_id)
        if not sub or sub["status"] != "active":
            return {"success": False, "details": "Subscription not active"}

        if sub["max_periods"] > 0 and sub["periods_paid"] >= sub["max_periods"]:
            sub["status"] = "expired"
            return {"success": False, "details": "Subscription expired"}

        # Process payment
        try:
            txn = ledger.transfer(
                from_agent=sub["subscriber"],
                to_agent=sub["provider"],
                amount=sub["price"],
                contract_id=contract_id,
                reason=f"Subscription payment period {sub['periods_paid'] + 1}",
            )
            sub["periods_paid"] += 1
            return {"success": True, "transaction": txn, "period": sub["periods_paid"]}
        except ValueError as e:
            sub["status"] = "payment_failed"
            return {"success": False, "details": str(e)}

    def cancel_subscription(self, contract_id: str, reason: str = "") -> dict:
        """Cancel an active subscription."""
        sub = self._active_subscriptions.get(contract_id)
        if not sub:
            return {"success": False, "details": "Subscription not found"}

        sub["status"] = "cancelled"
        contract = self.contract_mgr.get_contract(contract_id)
        if contract:
            self.contract_mgr.cancel(
                contract_id, sub["subscriber"], reason or "Subscription cancelled"
            )
        return {"success": True, "details": "Subscription cancelled"}

    def get_active_subscriptions(self, agent_id: str) -> list[dict[str, Any]]:
        """Get all active subscriptions for an agent (as subscriber)."""
        return [
            sub for sub in self._active_subscriptions.values()
            if sub["subscriber"] == agent_id and sub["status"] == "active"
        ]
