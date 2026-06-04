"""
ACP Team Formation.

Temporary multi-agent team assembly and coordination.
Enables agents to form ad-hoc teams for complex outcomes
that no single agent can deliver alone.

Flow: Assemble → Coordinate → Deliver → Payout → Disband
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from acp.protocol.models import Team, TeamMember, TeamRole


class TeamStatus(str, Enum):
    FORMING = "forming"
    ACTIVE = "active"
    DELIVERING = "delivering"
    COMPLETED = "completed"
    DISBANDED = "disbanded"


@dataclass
class TaskAssignment:
    """A task assigned to a team member."""

    task_id: str
    assignee_id: str
    description: str
    dependencies: list[str] = field(default_factory=list)  # task_ids that must complete first
    status: str = "pending"  # pending / in_progress / completed / blocked
    deliverable: Any = None
    assigned_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    completed_at: str | None = None


class TeamManager:
    """
    Manages the lifecycle of temporary agent teams.

    Coordinates task assignment, dependency tracking, progress
    monitoring, and final payout distribution.
    """

    def __init__(self) -> None:
        self._teams: dict[str, Team] = {}
        self._tasks: dict[str, list[TaskAssignment]] = {}

    # ── Team Lifecycle ─────────────────────────────────────

    def form_team(
        self,
        name: str,
        contract_id: str = "",
        members: list[dict[str, Any]] | None = None,
    ) -> Team:
        """
        Form a new team.

        Args:
            name: Team name.
            contract_id: The contract this team is fulfilling.
            members: List of {agent_id, role, payout_share} dicts.

        Returns:
            The created Team.
        """
        import uuid

        team = Team(
            team_id=f"team-{uuid.uuid4().hex[:12]}",
            name=name,
            contract_id=contract_id,
            status=TeamStatus.FORMING.value,
        )

        if members:
            for m in members:
                team.members.append(TeamMember(
                    agent_id=m["agent_id"],
                    role=TeamRole(m.get("role", "member")),
                    payout_share=m.get("payout_share", 0.0),
                ))

        self._teams[team.team_id] = team
        self._tasks[team.team_id] = []
        return team

    def activate(self, team_id: str) -> Team:
        """Activate a team (move from forming to active)."""
        team = self._get_team(team_id)
        if team.status != TeamStatus.FORMING.value:
            raise ValueError(f"Team {team_id} is not in forming status")
        if not team.members:
            raise ValueError("Cannot activate team with no members")
        team.status = TeamStatus.ACTIVE.value
        return team

    def disband(self, team_id: str) -> Team:
        """Disband a team after completion."""
        team = self._get_team(team_id)
        team.status = TeamStatus.DISBANDED.value
        return team

    # ── Task Management ────────────────────────────────────

    def assign_task(
        self,
        team_id: str,
        assignee_id: str,
        description: str,
        dependencies: list[str] | None = None,
    ) -> TaskAssignment:
        """Assign a task to a team member."""
        team = self._get_team(team_id)

        # Verify assignee is a team member
        if not any(m.agent_id == assignee_id for m in team.members):
            raise ValueError(f"Agent {assignee_id} is not a member of team {team_id}")

        import uuid
        task = TaskAssignment(
            task_id=f"task-{uuid.uuid4().hex[:12]}",
            assignee_id=assignee_id,
            description=description,
            dependencies=dependencies or [],
        )
        self._tasks[team_id].append(task)

        # Update member's assigned tasks
        for member in team.members:
            if member.agent_id == assignee_id:
                member.assigned_tasks.append(task.task_id)

        return task

    def complete_task(
        self, team_id: str, task_id: str, deliverable: Any = None
    ) -> TaskAssignment:
        """Mark a task as completed."""
        task = self._get_task(team_id, task_id)
        task.status = "completed"
        task.deliverable = deliverable
        task.completed_at = datetime.now(UTC).isoformat()

        # Check if all tasks are done
        all_done = all(
            t.status == "completed" for t in self._tasks[team_id]
        )
        if all_done:
            team = self._get_team(team_id)
            team.status = TeamStatus.COMPLETED.value

        return task

    def block_task(self, team_id: str, task_id: str, reason: str) -> TaskAssignment:
        """Mark a task as blocked (waiting on dependency or external factor)."""
        task = self._get_task(team_id, task_id)
        task.status = "blocked"
        return task

    # ── Progress & Status ──────────────────────────────────

    def get_team_progress(self, team_id: str) -> dict[str, Any]:
        """Get a progress summary for a team."""
        tasks = self._tasks.get(team_id, [])
        if not tasks:
            return {"total": 0, "completed": 0, "in_progress": 0, "blocked": 0, "done": False}

        status_counts = {"completed": 0, "in_progress": 0, "pending": 0, "blocked": 0}
        for t in tasks:
            status_counts[t.status] = status_counts.get(t.status, 0) + 1

        return {
            "total": len(tasks),
            **status_counts,
            "done": status_counts["completed"] == len(tasks),
        }

    def get_next_ready_tasks(self, team_id: str) -> list[TaskAssignment]:
        """Get tasks whose dependencies are all satisfied."""
        tasks = self._tasks.get(team_id, [])
        completed_ids = {t.task_id for t in tasks if t.status == "completed"}

        ready = []
        for t in tasks:
            if t.status == "pending" and all(
                dep in completed_ids for dep in t.dependencies
            ):
                ready.append(t)

        return ready

    # ── Payout Calculation ─────────────────────────────────

    def calculate_payouts(
        self, team_id: str, total_payment: float
    ) -> dict[str, float]:
        """
        Calculate payout for each team member based on their share.

        Returns {agent_id: amount} dict.
        """
        team = self._get_team(team_id)
        payouts: dict[str, float] = {}

        total_shares = sum(m.payout_share for m in team.members)
        if total_shares == 0:
            # Equal split if no shares defined
            share = total_payment / max(len(team.members), 1)
            for m in team.members:
                payouts[m.agent_id] = round(share, 2)
        else:
            for m in team.members:
                payouts[m.agent_id] = round(
                    total_payment * (m.payout_share / total_shares), 2
                )

        return payouts

    # ── Query ──────────────────────────────────────────────

    def get_team(self, team_id: str) -> Team | None:
        return self._teams.get(team_id)

    def get_agent_teams(self, agent_id: str) -> list[Team]:
        """Get all teams an agent is a member of."""
        return [
            t for t in self._teams.values()
            if any(m.agent_id == agent_id for m in t.members)
        ]

    def get_tasks(self, team_id: str) -> list[TaskAssignment]:
        return list(self._tasks.get(team_id, []))

    # ── Helpers ────────────────────────────────────────────

    def _get_team(self, team_id: str) -> Team:
        team = self._teams.get(team_id)
        if team is None:
            raise KeyError(f"Team not found: {team_id}")
        return team

    def _get_task(self, team_id: str, task_id: str) -> TaskAssignment:
        tasks = self._tasks.get(team_id, [])
        for t in tasks:
            if t.task_id == task_id:
                return t
        raise KeyError(f"Task not found: {task_id}")

    @property
    def total_teams(self) -> int:
        return len(self._teams)
