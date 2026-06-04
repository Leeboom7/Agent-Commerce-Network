"""
ACP Relationship: Commission.

Delegate a sub-task to another agent as part of a larger workflow.
The commissioning agent (principal) outsources a well-defined task
to a commissioned agent, who delivers the result.

Example: An orchestrator agent commissions a translation agent to
translate a document as part of a report-generation workflow.
"""

from __future__ import annotations

from typing import Any

from acp.contract.manager import ContractManager
from acp.negotiation.engine import NegotiationEngine, NegotiationOutcome
from acp.negotiation.strategies import BaseNegotiationStrategy, create_strategy
from acp.protocol.models import MarketContext


class CommissionRelationship:
    """
    Implements the 'commission' economic relationship type.

    Flow:
    1. Principal defines the sub-task with clear deliverables
    2. Principal discovers commissioned agent via Registry
    3. Principal and agent negotiate scope and price
    4. Contract is created with task specification
    5. Commissioned agent delivers
    6. Principal reviews and accepts/rejects
    7. Payment is settled

    Key difference from Purchase: Commission implies the task is
    part of a larger workflow controlled by the principal.
    """

    def __init__(
        self,
        engine: NegotiationEngine | None = None,
        contract_mgr: ContractManager | None = None,
    ) -> None:
        self.engine = engine or NegotiationEngine()
        self.contract_mgr = contract_mgr or ContractManager()

    async def commission(
        self,
        principal_id: str,
        agent_id: str,
        task_spec: dict[str, Any],
        principal_strategy: BaseNegotiationStrategy | None = None,
        agent_strategy: BaseNegotiationStrategy | None = None,
        market_context: MarketContext | None = None,
    ) -> dict:
        """
        Commission a sub-task to another agent.

        Args:
            principal_id: The agent delegating the work.
            agent_id: The agent being commissioned.
            task_spec: Description of the sub-task, deliverables, and requirements.
            principal_strategy: Negotiation strategy for the principal.
            agent_strategy: Negotiation strategy for the commissioned agent.
            market_context: Market data.

        Returns:
            dict with success, contract, outcome, and details.
        """
        context = market_context or MarketContext()

        # Build contract terms from task specification
        estimated_price = task_spec.get("estimated_price", 50.0)

        if principal_strategy is None:
            principal_strategy = create_strategy(
                "tit-for-tat",
                reservation_price=estimated_price * 1.5,
                opening_price=estimated_price * 0.6,
            )
        if agent_strategy is None:
            agent_strategy = create_strategy(
                "value-based",
                base_price=estimated_price,
                value_multiplier=1.2,
            )

        # Negotiate
        session = self.engine.start_session(principal_id, agent_id, "commission")
        outcome: NegotiationOutcome = await self.engine.negotiate(
            session,
            principal_strategy,
            agent_strategy,
            context,
        )

        if outcome.agreed_terms is None:
            self.engine.close_session(session.session_id)
            return {
                "success": False,
                "contract": None,
                "outcome": outcome,
                "details": f"Commission negotiation failed: {outcome.outcome_type.value}",
            }

        # Embed task spec in contract terms metadata
        agreed_terms = outcome.agreed_terms
        agreed_terms.metadata["task_spec"] = task_spec
        agreed_terms.deliverables = task_spec.get("deliverables", [])

        # Create and sign contract
        contract = self.contract_mgr.create_contract(
            buyer_id=principal_id,
            seller_id=agent_id,
            relationship_type="commission",
            terms=agreed_terms,
            negotiation_session_id=session.session_id,
        )
        self.contract_mgr.sign(contract.contract_id, principal_id)
        self.contract_mgr.sign(contract.contract_id, agent_id)

        self.engine.close_session(session.session_id)

        return {
            "success": True,
            "contract": contract,
            "outcome": outcome,
            "details": (
                f"Commission: {principal_id} → {agent_id} "
                f"({task_spec.get('description', 'unnamed task')}) "
                f"for {agreed_terms.price} NC. "
                f"Contract: {contract.contract_id}"
            ),
        }
