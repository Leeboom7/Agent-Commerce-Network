"""
ACP Relationship: Arbitration.

Resolve disputes between transacting agents through binding arbitration.
An independent arbitrator agent reviews the contract, delivery, and
evidence, then issues a ruling that is automatically enforced.

Example: Buyer claims delivery was substandard. Seller claims it met spec.
Both agree to binding arbitration. The arbitrator reviews and rules.
"""

from __future__ import annotations

from typing import Any

from acp.arbitration.arbitrator import ArbitrationEngine
from acp.contract.manager import ContractManager
from acp.negotiation.engine import NegotiationEngine
from acp.negotiation.strategies import create_strategy
from acp.protocol.models import MarketContext, ServiceContract, VerificationReport


class ArbitrationRelationship:
    """
    Implements the 'arbitration' economic relationship type.

    Flow:
    1. Transacting parties (or one of them) initiate arbitration
    2. An arbitrator agent is engaged
    3. Arbitrator reviews evidence (contract, delivery, verification report)
    4. Arbitrator issues a binding ruling
    5. Ruling is enforced (refund, penalty, revision requirement)
    6. Arbitrator is paid for the service
    """

    def __init__(
        self,
        engine: NegotiationEngine | None = None,
        contract_mgr: ContractManager | None = None,
    ) -> None:
        self.engine = engine or NegotiationEngine()
        self.contract_mgr = contract_mgr or ContractManager()
        self._arbitrator = ArbitrationEngine()

    async def resolve_dispute(
        self,
        contract: ServiceContract,
        claimant_id: str,
        claim: str,
        arbitrator_id: str,
        evidence: dict[str, Any] | None = None,
        verification_report: VerificationReport | None = None,
        market_context: MarketContext | None = None,
    ) -> dict:
        """
        File and resolve a dispute through arbitration.

        Args:
            contract: The disputed contract.
            claimant_id: Agent filing the dispute.
            claim: Description of what went wrong.
            arbitrator_id: The arbitrator agent.
            evidence: Any supporting evidence.
            verification_report: Optional verification report.
            market_context: Market data.

        Returns:
            dict with success, ruling, contract_updates, details.
        """
        # File the case
        case = self._arbitrator.file_case(
            contract=contract,
            claimant_id=claimant_id,
            claim=claim,
            evidence=evidence,
            verification_report=verification_report,
        )

        # Rule on the case
        ruling = self._arbitrator.rule(
            case_id=case.case_id,
            arbitrator_id=arbitrator_id,
            contract=contract,
        )

        # Enforce the ruling on the contract
        contract_updates = self._enforce_ruling(contract, ruling)

        # Create a mini-contract for the arbitration service
        context = market_context or MarketContext()
        arb_fee = 10.0  # Fixed arbitration fee in MVP

        from acp.protocol.models import ContractTerms
        arb_contract = self.contract_mgr.create_contract(
            buyer_id=claimant_id,
            seller_id=arbitrator_id,
            relationship_type="arbitration",
            terms=ContractTerms(price=arb_fee, deadline=""),
        )
        self.contract_mgr.sign(arb_contract.contract_id, claimant_id)
        self.contract_mgr.sign(arb_contract.contract_id, arbitrator_id)
        self.contract_mgr.deliver(
            arb_contract.contract_id, arbitrator_id,
            {"ruling": ruling},
        )
        self.contract_mgr.accept(arb_contract.contract_id, claimant_id)

        return {
            "success": True,
            "case_id": case.case_id,
            "ruling": ruling,
            "contract_updates": contract_updates,
            "arbitration_fee": arb_fee,
            "details": (
                f"Arbitration complete: {ruling.ruling_type.value}. "
                f"Remedy: {ruling.remedy['action']}. "
                f"Fee: {arb_fee} NC."
            ),
        }

    def _enforce_ruling(
        self, contract: ServiceContract, ruling: Any
    ) -> dict[str, Any]:
        """Enforce an arbitration ruling on the contract."""
        updates: dict[str, Any] = {
            "contract_id": contract.contract_id,
            "ruling_type": ruling.ruling_type.value,
            "remedy": ruling.remedy,
        }

        remedy = ruling.remedy
        action = remedy.get("action", "")

        if action == "refund" or action == "partial_refund":
            self.contract_mgr.resolve(
                contract.contract_id,
                ruling.arbitrator_id,
                {"verdict": action, "ruling_id": ruling.ruling_id},
            )
            updates["contract_resolved"] = True
            updates["penalty_to_seller"] = remedy.get("penalty_to_seller", 0)

        elif action == "revision_required":
            # Keep contract active, seller must revise
            updates["contract_resolved"] = False
            updates["revision_deadline_hours"] = remedy.get(
                "deadline_extension_hours", 48
            )

        elif action == "no_refund":
            self.contract_mgr.resolve(
                contract.contract_id,
                ruling.arbitrator_id,
                {"verdict": "claim_rejected", "ruling_id": ruling.ruling_id},
            )
            updates["contract_resolved"] = True
            updates["penalty_to_buyer"] = remedy.get("penalty_to_buyer", 0)

        return updates
