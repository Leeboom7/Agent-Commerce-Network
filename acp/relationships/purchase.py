"""
ACP Relationship: Purchase.

Buy a fixed service or product from another agent.
The simplest and most fundamental economic relationship.

Example: Agent A pays Agent B 50 NC for a market data report.
"""

from __future__ import annotations

from acp.contract.manager import ContractManager
from acp.negotiation.engine import NegotiationEngine, NegotiationOutcome
from acp.protocol.models import MarketContext
from acp.negotiation.strategies import BaseNegotiationStrategy, create_strategy
from acp.protocol.models import ContractTerms, ServiceContract


class PurchaseRelationship:
    """
    Implements the 'purchase' economic relationship type.

    Flow:
    1. Buyer discovers seller via Registry
    2. Buyer and seller negotiate price/terms
    3. Contract is created and signed
    4. Seller delivers the service/product
    5. Buyer accepts (or rejects) the delivery
    6. Payment is settled
    """

    def __init__(
        self,
        engine: NegotiationEngine | None = None,
        contract_mgr: ContractManager | None = None,
    ) -> None:
        self.engine = engine or NegotiationEngine()
        self.contract_mgr = contract_mgr or ContractManager()

    async def execute(
        self,
        buyer_id: str,
        seller_id: str,
        buyer_strategy: BaseNegotiationStrategy | None = None,
        seller_strategy: BaseNegotiationStrategy | None = None,
        market_context: MarketContext | None = None,
    ) -> dict:
        """
        Execute a complete purchase transaction.

        Returns a dict with:
        - success: bool
        - contract: ServiceContract (if successful)
        - outcome: NegotiationOutcome
        - details: str
        """
        context = market_context or MarketContext()

        # Default strategies if not provided
        if buyer_strategy is None:
            buyer_strategy = create_strategy(
                "batna", batna_value=50.0, target_price=70.0
            )
        if seller_strategy is None:
            seller_strategy = create_strategy(
                "concession", reservation_price=40.0, opening_price=100.0
            )

        # 1. Negotiate
        session = self.engine.start_session(buyer_id, seller_id, "purchase")
        outcome: NegotiationOutcome = await self.engine.negotiate(
            session, buyer_strategy, seller_strategy, context
        )

        if outcome.agreed_terms is None:
            self.engine.close_session(session.session_id)
            return {
                "success": False,
                "contract": None,
                "outcome": outcome,
                "details": f"Negotiation failed: {outcome.outcome_type.value}",
            }

        # 2. Create and sign contract
        contract = self.contract_mgr.create_contract(
            buyer_id=buyer_id,
            seller_id=seller_id,
            relationship_type="purchase",
            terms=outcome.agreed_terms,
            negotiation_session_id=session.session_id,
        )
        self.contract_mgr.sign(contract.contract_id, buyer_id)
        self.contract_mgr.sign(contract.contract_id, seller_id)

        self.engine.close_session(session.session_id)

        return {
            "success": True,
            "contract": contract,
            "outcome": outcome,
            "details": (
                f"Purchase agreement: {buyer_id} pays {seller_id} "
                f"{outcome.agreed_terms.price} NC. "
                f"Contract: {contract.contract_id}"
            ),
        }
