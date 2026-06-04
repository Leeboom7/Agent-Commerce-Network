"""
ACP Relationship: Team Formation.

Multiple agents form a temporary team for a complex outcome that
no single agent can deliver alone. The team assembles, coordinates
via task assignments, delivers, and disbands with payout distribution.

Example: To generate a comprehensive industry report, an orchestrator
assembles: data analyst + report writer + fact checker + designer.
"""

from __future__ import annotations

from typing import Any

from acp.contract.manager import ContractManager
from acp.negotiation.engine import NegotiationEngine
from acp.protocol.models import MarketContext
from acp.team.formation import Team, TeamManager, TeamStatus


class TeamFormationRelationship:
    """
    Implements the 'team_formation' economic relationship type.

    Flow:
    1. Orchestrator posts a complex task
    2. Orchestrator discovers and recruits agents
    3. Team is formed with defined roles and payout shares
    4. Tasks are assigned with dependency tracking
    5. Members execute tasks (potentially in parallel)
    6. Orchestrator verifies and integrates deliverables
    7. Final delivery to client
    8. Payout distributed per agreed shares
    9. Team disbands
    """

    def __init__(
        self,
        engine: NegotiationEngine | None = None,
        contract_mgr: ContractManager | None = None,
    ) -> None:
        self.engine = engine or NegotiationEngine()
        self.contract_mgr = contract_mgr or ContractManager()
        self._team_mgr = TeamManager()

    def assemble_team(
        self,
        name: str,
        contract_id: str = "",
        members: list[dict[str, Any]] | None = None,
    ) -> Team:
        """
        Assemble a team for a complex task.

        Args:
            name: Team name describing the mission.
            contract_id: Associated contract (if any).
            members: List of {agent_id, role, payout_share} dicts.

        Returns:
            The formed Team.
        """
        team = self._team_mgr.form_team(
            name=name,
            contract_id=contract_id,
            members=members,
        )
        self._team_mgr.activate(team.team_id)
        return team

    def assign_tasks(
        self,
        team_id: str,
        task_assignments: list[dict[str, Any]],
    ) -> list[Any]:
        """
        Assign tasks to team members with dependency tracking.

        Args:
            team_id: The team to assign tasks to.
            task_assignments: List of {assignee_id, description, dependencies} dicts.

        Returns:
            List of created TaskAssignments.
        """
        tasks = []
        for ta in task_assignments:
            task = self._team_mgr.assign_task(
                team_id=team_id,
                assignee_id=ta["assignee_id"],
                description=ta["description"],
                dependencies=ta.get("dependencies", []),
            )
            tasks.append(task)

        # Log dependencies as blocked until prerequisites complete
        for task in tasks:
            if task.dependencies:
                ready = all(
                    dep in {
                        t.task_id
                        for t in self._team_mgr.get_tasks(team_id)
                        if t.status == "completed"
                    }
                    for dep in task.dependencies
                )
                if not ready:
                    self._team_mgr.block_task(
                        team_id, task.task_id,
                        f"Waiting for dependencies: {task.dependencies}"
                    )

        return tasks

    def complete_task(
        self, team_id: str, task_id: str, deliverable: Any = None
    ) -> Any:
        """Mark a team task as completed."""
        return self._team_mgr.complete_task(team_id, task_id, deliverable)

    def get_ready_tasks(self, team_id: str) -> list[Any]:
        """Get tasks that are unblocked and ready to execute."""
        return self._team_mgr.get_next_ready_tasks(team_id)

    def get_progress(self, team_id: str) -> dict[str, Any]:
        """Get team progress summary."""
        return self._team_mgr.get_team_progress(team_id)

    def finalize_team(
        self, team_id: str, total_payment: float
    ) -> dict:
        """
        Calculate payouts and disband the team.

        Returns payout distribution.
        """
        payouts = self._team_mgr.calculate_payouts(team_id, total_payment)
        self._team_mgr.disband(team_id)
        return {
            "success": True,
            "team_id": team_id,
            "payouts": payouts,
            "total": total_payment,
            "details": f"Team disbanded. {len(payouts)} members paid.",
        }

    def get_team(self, team_id: str) -> Team | None:
        return self._team_mgr.get_team(team_id)
