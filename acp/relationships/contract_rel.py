"""
ACP Relationship: Contract (Formal).

Formal project-based delivery with milestones and acceptance criteria.
The most structured discrete transaction type.

Example: A buyer agent contracts a developer agent to build a complete
web scraper with 3 defined milestones, each with its own acceptance
criteria and payment schedule.
"""

from __future__ import annotations

from typing import Any

from acp.contract.manager import ContractManager
from acp.negotiation.engine import NegotiationEngine, NegotiationOutcome
from acp.negotiation.strategies import BaseNegotiationStrategy, create_strategy
from acp.protocol.models import MarketContext


class ContractRelationship:
    """
    Implements the 'contract' economic relationship type.

    Flow:
    1. Buyer defines project scope with milestones
    2. Buyer and seller negotiate overall price + milestone schedule
    3. Contract is created with milestone-based terms
    4. Seller delivers milestone by milestone
    5. Buyer accepts each milestone (or rejects with feedback)
    6. Payment is released per milestone (in production: via escrow)
    7. Final acceptance triggers full settlement
    """

    def __init__(
        self,
        engine: NegotiationEngine | None = None,
        contract_mgr: ContractManager | None = None,
    ) -> None:
        self.engine = engine or NegotiationEngine()
        self.contract_mgr = contract_mgr or ContractManager()
        self._milestone_status: dict[str, list[dict[str, Any]]] = {}

    async def negotiate_and_sign(
        self,
        buyer_id: str,
        seller_id: str,
        project_spec: dict[str, Any],
        buyer_strategy: BaseNegotiationStrategy | None = None,
        seller_strategy: BaseNegotiationStrategy | None = None,
        market_context: MarketContext | None = None,
    ) -> dict:
        """
        Negotiate and sign a formal project contract.

        Args:
            buyer_id: The agent procuring the work.
            seller_id: The agent performing the work.
            project_spec: Complete project specification including:
                - description: str
                - milestones: list of {name, description, deliverables, acceptance_criteria, payment_share}
                - total_budget: float
                - deadline: str (ISO 8601)
            buyer_strategy: Negotiation strategy for buyer.
            seller_strategy: Negotiation strategy for seller.
            market_context: Market data.

        Returns:
            dict with success, contract, outcome, details.
        """
        context = market_context or MarketContext()
        total_budget = project_spec.get("total_budget", 200.0)
        milestones = project_spec.get("milestones", [])

        if not milestones:
            return {
                "success": False,
                "contract": None,
                "outcome": None,
                "details": "Project must have at least one milestone.",
            }

        if buyer_strategy is None:
            buyer_strategy = create_strategy(
                "batna",
                batna_value=total_budget * 0.6,
                target_price=total_budget * 0.8,
            )
        if seller_strategy is None:
            seller_strategy = create_strategy(
                "concession",
                reservation_price=total_budget * 0.6,
                opening_price=total_budget,
            )

        # Negotiate
        session = self.engine.start_session(buyer_id, seller_id, "contract")
        outcome: NegotiationOutcome = await self.engine.negotiate(
            session, buyer_strategy, seller_strategy, context
        )

        if outcome.agreed_terms is None:
            self.engine.close_session(session.session_id)
            return {
                "success": False,
                "contract": None,
                "outcome": outcome,
                "details": f"Contract negotiation failed: {outcome.outcome_type.value}",
            }

        # Embed project spec in contract
        agreed_terms = outcome.agreed_terms
        agreed_terms.metadata["project_spec"] = project_spec
        agreed_terms.metadata["milestones"] = milestones

        # Create and sign contract
        contract = self.contract_mgr.create_contract(
            buyer_id=buyer_id,
            seller_id=seller_id,
            relationship_type="contract",
            terms=agreed_terms,
            negotiation_session_id=session.session_id,
        )
        self.contract_mgr.sign(contract.contract_id, buyer_id)
        self.contract_mgr.sign(contract.contract_id, seller_id)

        # Initialize milestone tracking
        self._milestone_status[contract.contract_id] = [
            {"index": i, "name": m["name"], "status": "pending", "delivery": None}
            for i, m in enumerate(milestones)
        ]

        self.engine.close_session(session.session_id)

        return {
            "success": True,
            "contract": contract,
            "outcome": outcome,
            "details": (
                f"Formal contract: {buyer_id} ↔ {seller_id}, "
                f"{len(milestones)} milestones, "
                f"{agreed_terms.price} NC total. "
                f"Contract: {contract.contract_id}"
            ),
        }

    def deliver_milestone(
        self,
        contract_id: str,
        milestone_index: int,
        delivery: dict[str, Any],
    ) -> dict:
        """
        Record delivery of a specific milestone.

        Returns milestone status.
        """
        if contract_id not in self._milestone_status:
            return {"success": False, "details": "Contract not found in milestone tracker"}

        milestones = self._milestone_status[contract_id]
        if milestone_index >= len(milestones):
            return {"success": False, "details": "Invalid milestone index"}

        milestone = milestones[milestone_index]
        if milestone["status"] not in ("pending", "rejected"):
            return {"success": False, "details": f"Milestone already {milestone['status']}"}

        milestone["status"] = "delivered"
        milestone["delivery"] = delivery

        # Also update the main contract
        contract = self.contract_mgr.get_contract(contract_id)
        if contract:
            self.contract_mgr.deliver(contract_id, contract.seller_id, {
                "milestone_index": milestone_index,
                "milestone_name": milestone["name"],
                "delivery": delivery,
            })

        return {"success": True, "milestone": milestone}

    def accept_milestone(
        self, contract_id: str, milestone_index: int
    ) -> dict:
        """Accept a delivered milestone."""
        if contract_id not in self._milestone_status:
            return {"success": False, "details": "Contract not found"}

        milestone = self._milestone_status[contract_id][milestone_index]
        if milestone["status"] != "delivered":
            return {"success": False, "details": f"Milestone is {milestone['status']}, not delivered"}

        milestone["status"] = "accepted"

        # Check if all milestones are accepted
        all_accepted = all(m["status"] == "accepted" for m in self._milestone_status[contract_id])
        if all_accepted:
            contract = self.contract_mgr.get_contract(contract_id)
            if contract:
                self.contract_mgr.accept(contract_id, contract.buyer_id)

        return {"success": True, "milestone": milestone, "all_complete": all_accepted}

    def get_milestones(self, contract_id: str) -> list[dict[str, Any]]:
        """Get milestone status for a contract."""
        return list(self._milestone_status.get(contract_id, []))
