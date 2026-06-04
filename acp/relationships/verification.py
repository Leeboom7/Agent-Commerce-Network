"""
ACP Relationship: Verification.

Verify or audit another agent's delivery against contract terms.
A specialized third-party agent checks whether a seller's delivery
meets the acceptance criteria defined in the contract.

Example: Before releasing payment, the buyer commissions a verifier
agent to check that all acceptance criteria are met.
"""

from __future__ import annotations

from typing import Any

from acp.contract.manager import ContractManager
from acp.negotiation.engine import NegotiationEngine
from acp.negotiation.strategies import BaseNegotiationStrategy, create_strategy
from acp.protocol.models import MarketContext
from acp.verification.verifier import DeliveryVerifier


class VerificationRelationship:
    """
    Implements the 'verification' economic relationship type.

    Flow:
    1. Buyer or seller requests verification from a verifier agent
    2. Verifier examines the delivery against contract criteria
    3. Verifier produces a VerificationReport
    4. Report is used to accept/reject the delivery
    5. Verifier is paid for the service
    """

    def __init__(
        self,
        engine: NegotiationEngine | None = None,
        contract_mgr: ContractManager | None = None,
    ) -> None:
        self.engine = engine or NegotiationEngine()
        self.contract_mgr = contract_mgr or ContractManager()
        self._verifier = DeliveryVerifier()

    async def request_verification(
        self,
        requester_id: str,
        verifier_id: str,
        contract_id: str,
        delivery: dict[str, Any],
        verifier_strategy: BaseNegotiationStrategy | None = None,
        market_context: MarketContext | None = None,
    ) -> dict:
        """
        Request verification of a delivery.

        Args:
            requester_id: Agent requesting verification (usually buyer).
            verifier_id: Agent performing verification.
            contract_id: The contract whose delivery needs verification.
            delivery: The actual deliverable to check.
            verifier_strategy: Negotiation strategy for the verifier.
            market_context: Market data.

        Returns:
            dict with success, verification_report, contract, details.
        """
        # Get the contract
        contract = self.contract_mgr.get_contract(contract_id)
        if contract is None:
            return {"success": False, "details": f"Contract {contract_id} not found"}

        criteria = contract.terms.acceptance_criteria
        if not criteria:
            return {
                "success": False,
                "details": "Contract has no acceptance criteria to verify",
            }

        # Negotiate verification fee (simplified: small fixed negotiation)
        context = market_context or MarketContext()
        if verifier_strategy is None:
            verifier_strategy = create_strategy(
                "value-based", base_price=20.0, value_multiplier=1.0
            )

        session = self.engine.start_session(
            requester_id, verifier_id, "verification"
        )

        # Simple fixed-price negotiation for verification
        requester_strategy = create_strategy(
            "tit-for-tat", reservation_price=30.0, opening_price=10.0
        )

        outcome = await self.engine.negotiate(
            session, requester_strategy, verifier_strategy, context,
        )

        # Even if negotiation "fails", we still do verification (simplified)
        # In production, verification would require agreed payment
        verification_fee = (
            outcome.agreed_terms.price
            if outcome.agreed_terms
            else 20.0
        )

        # Perform verification
        report = self._verifier.verify(
            contract_id=contract_id,
            verifier_id=verifier_id,
            delivery=delivery,
            criteria=criteria,
        )

        # Create a mini-contract for the verification service
        from acp.protocol.models import ContractTerms
        v_contract = self.contract_mgr.create_contract(
            buyer_id=requester_id,
            seller_id=verifier_id,
            relationship_type="verification",
            terms=ContractTerms(
                price=verification_fee,
                deadline="",
                deliverables=["verification_report"],
                acceptance_criteria=["Report must cover all contract criteria"],
            ),
        )
        self.contract_mgr.sign(v_contract.contract_id, requester_id)
        self.contract_mgr.sign(v_contract.contract_id, verifier_id)

        # Auto-deliver and accept the verification
        self.contract_mgr.deliver(
            v_contract.contract_id, verifier_id,
            {"verification_report": report},
        )
        self.contract_mgr.accept(v_contract.contract_id, requester_id)

        self.engine.close_session(session.session_id)

        return {
            "success": True,
            "verification_report": report,
            "verification_contract": v_contract,
            "verification_fee": verification_fee,
            "verdict": report.verdict,
            "details": (
                f"Verification complete: {report.verdict}. "
                f"{report.pass_rate*100:.0f}% criteria passed. "
                f"Fee: {verification_fee} NC."
            ),
        }
