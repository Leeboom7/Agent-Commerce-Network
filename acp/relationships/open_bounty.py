"""
ACP Relationship: Open Bounty.

Post a task publicly; agents compete or bid to win the work.
The most marketplace-like relationship type — price discovery
happens through competitive bidding rather than bilateral negotiation.

Example: Orchestrator posts "Build a SQL query optimizer, budget 200 NC."
Three developer agents submit proposals. Orchestrator picks the winner.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class BountyProposal:
    """A proposal submitted by an agent in response to a bounty."""

    proposal_id: str
    bounty_id: str
    bidder_id: str
    price: float
    description: str
    estimated_duration: str = ""
    bidder_reputation: float = 100.0
    submitted_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class OpenBountyRelationship:
    """
    Implements the 'open bounty' economic relationship type.

    Flow:
    1. Requester posts a bounty with description, budget, and deadline
    2. Agents discover the bounty and submit proposals
    3. After the submission window, the requester evaluates proposals
    4. Winner is selected (based on price, reputation, proposal quality)
    5. Contract is created between requester and winner
    6. Winner delivers, requester accepts, payment settles
    """

    def __init__(self) -> None:
        self._bounties: dict[str, dict[str, Any]] = {}
        self._proposals: dict[str, list[BountyProposal]] = {}

    def post_bounty(
        self,
        requester_id: str,
        title: str,
        description: str,
        budget: float,
        deadline: str,
        requirements: list[str] | None = None,
        submission_window_hours: int = 48,
    ) -> str:
        """
        Post a new bounty. Returns the bounty_id.

        Args:
            requester_id: Agent posting the bounty.
            title: Short title of the task.
            description: Detailed description of what needs to be done.
            budget: Maximum price the requester is willing to pay.
            deadline: When the work must be completed (ISO 8601).
            requirements: List of specific requirements the winner must meet.
            submission_window_hours: How long agents have to submit proposals.
        """
        import uuid

        bounty_id = f"bounty-{uuid.uuid4().hex[:12]}"
        now = datetime.now(UTC)

        self._bounties[bounty_id] = {
            "bounty_id": bounty_id,
            "requester_id": requester_id,
            "title": title,
            "description": description,
            "budget": budget,
            "deadline": deadline,
            "requirements": requirements or [],
            "status": "open",
            "created_at": now.isoformat(),
            "submission_deadline": datetime.fromtimestamp(
                now.timestamp() + submission_window_hours * 3600, tz=UTC
            ).isoformat(),
            "winner_id": None,
            "winning_proposal_id": None,
        }
        self._proposals[bounty_id] = []
        return bounty_id

    def submit_proposal(
        self,
        bounty_id: str,
        bidder_id: str,
        price: float,
        description: str,
        estimated_duration: str = "",
        bidder_reputation: float = 100.0,
    ) -> dict:
        """
        Submit a proposal for a bounty. Returns proposal result.
        """
        import uuid

        bounty = self._bounties.get(bounty_id)
        if bounty is None:
            return {"success": False, "details": "Bounty not found"}
        if bounty["status"] != "open":
            return {"success": False, "details": f"Bounty is {bounty['status']}"}

        # Check submission deadline
        deadline = datetime.fromisoformat(bounty["submission_deadline"])
        if datetime.now(UTC) > deadline:
            bounty["status"] = "evaluating"
            return {"success": False, "details": "Submission window has closed"}

        # Validate budget
        if price > bounty["budget"]:
            return {
                "success": False,
                "details": f"Proposal price ({price}) exceeds budget ({bounty['budget']})",
            }

        proposal = BountyProposal(
            proposal_id=f"prop-{uuid.uuid4().hex[:12]}",
            bounty_id=bounty_id,
            bidder_id=bidder_id,
            price=price,
            description=description,
            estimated_duration=estimated_duration,
            bidder_reputation=bidder_reputation,
        )
        self._proposals[bounty_id].append(proposal)

        return {
            "success": True,
            "proposal_id": proposal.proposal_id,
            "details": f"Proposal submitted for bounty {bounty_id} at {price} NC",
        }

    def evaluate_and_award(
        self,
        bounty_id: str,
        selection_strategy: str = "best_value",
    ) -> dict:
        """
        Evaluate all proposals and select a winner.

        Selection strategies:
        - "lowest_price": Pick the cheapest.
        - "best_value": Weighted score = (budget-price)/budget * 0.5 + rep/100 * 0.5
        - "highest_reputation": Pick the highest-reputation bidder.
        """
        bounty = self._bounties.get(bounty_id)
        if bounty is None:
            return {"success": False, "details": "Bounty not found"}

        proposals = self._proposals.get(bounty_id, [])
        if not proposals:
            bounty["status"] = "no_bids"
            return {"success": False, "details": "No proposals received"}

        budget = bounty["budget"]

        if selection_strategy == "lowest_price":
            proposals.sort(key=lambda p: p.price)
        elif selection_strategy == "highest_reputation":
            proposals.sort(key=lambda p: p.bidder_reputation, reverse=True)
        elif selection_strategy == "best_value":
            proposals.sort(
                key=lambda p: (
                    (budget - p.price) / budget * 0.5
                    + p.bidder_reputation / 100 * 0.5
                ),
                reverse=True,
            )

        winner = proposals[0]
        bounty["status"] = "awarded"
        bounty["winner_id"] = winner.bidder_id
        bounty["winning_proposal_id"] = winner.proposal_id

        return {
            "success": True,
            "bounty_id": bounty_id,
            "winner_id": winner.bidder_id,
            "winning_price": winner.price,
            "proposal_description": winner.description,
            "total_proposals": len(proposals),
            "all_proposals": [
                {
                    "bidder": p.bidder_id,
                    "price": p.price,
                    "reputation": p.bidder_reputation,
                }
                for p in proposals
            ],
        }

    def get_bounty(self, bounty_id: str) -> dict[str, Any] | None:
        """Get bounty details."""
        return self._bounties.get(bounty_id)

    def get_proposals(self, bounty_id: str) -> list[BountyProposal]:
        """Get all proposals for a bounty."""
        return list(self._proposals.get(bounty_id, []))

    def list_open_bounties(self) -> list[dict[str, Any]]:
        """List all currently open bounties."""
        return [
            b for b in self._bounties.values()
            if b["status"] == "open"
        ]
