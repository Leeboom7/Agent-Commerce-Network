"""Tests for team formation and management."""

import pytest

from acp.team.formation import TeamManager, TeamStatus


class TestTeamManager:
    @pytest.fixture
    def mgr(self) -> TeamManager:
        return TeamManager()

    def test_form_team(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            name="Analysis Squad",
            contract_id="contract-1",
            members=[
                {"agent_id": "agent-1", "role": "lead", "payout_share": 0.4},
                {"agent_id": "agent-2", "role": "member", "payout_share": 0.3},
                {"agent_id": "agent-3", "role": "member", "payout_share": 0.3},
            ],
        )
        assert team.team_id.startswith("team-")
        assert team.name == "Analysis Squad"
        assert len(team.members) == 3
        assert team.status == TeamStatus.FORMING.value

    def test_activate_team(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            "Test Team",
            members=[{"agent_id": "a", "role": "lead", "payout_share": 1.0}],
        )
        mgr.activate(team.team_id)
        assert team.status == TeamStatus.ACTIVE.value

    def test_cannot_activate_empty_team(self, mgr: TeamManager) -> None:
        team = mgr.form_team("Empty Team")
        with pytest.raises(ValueError, match="no members"):
            mgr.activate(team.team_id)

    def test_assign_and_complete_task(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            "Task Team",
            members=[{"agent_id": "a", "role": "lead", "payout_share": 1.0}],
        )
        mgr.activate(team.team_id)

        task = mgr.assign_task(team.team_id, "a", "Build the report")
        assert task.task_id.startswith("task-")
        assert task.status == "pending"

        # Get next ready tasks
        ready = mgr.get_next_ready_tasks(team.team_id)
        assert len(ready) == 1

        # Complete
        completed = mgr.complete_task(team.team_id, task.task_id, {"report": "# Done"})
        assert completed.status == "completed"

        # Team should be completed
        progress = mgr.get_team_progress(team.team_id)
        assert progress["done"] is True
        assert team.status == TeamStatus.COMPLETED.value

    def test_task_with_dependencies(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            "Dep Team",
            members=[
                {"agent_id": "a", "role": "lead", "payout_share": 0.5},
                {"agent_id": "b", "role": "member", "payout_share": 0.5},
            ],
        )
        mgr.activate(team.team_id)

        # Task B depends on Task A
        task_a = mgr.assign_task(team.team_id, "a", "Gather data")
        task_b = mgr.assign_task(
            team.team_id, "b", "Analyze data",
            dependencies=[task_a.task_id],
        )

        # Only task_a is ready
        ready = mgr.get_next_ready_tasks(team.team_id)
        assert len(ready) == 1
        assert ready[0].task_id == task_a.task_id

        # Complete task_a → task_b should become ready
        mgr.complete_task(team.team_id, task_a.task_id, {"data": "..."})
        ready = mgr.get_next_ready_tasks(team.team_id)
        assert len(ready) == 1
        assert ready[0].task_id == task_b.task_id

    def test_assign_to_non_member(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            "Strict Team",
            members=[{"agent_id": "a", "role": "lead", "payout_share": 1.0}],
        )
        mgr.activate(team.team_id)

        with pytest.raises(ValueError, match="not a member"):
            mgr.assign_task(team.team_id, "outsider", "Do something")

    def test_calculate_payouts_equal(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            "Equal Team",
            members=[
                {"agent_id": "a", "role": "lead", "payout_share": 0},
                {"agent_id": "b", "role": "member", "payout_share": 0},
            ],
        )
        mgr.activate(team.team_id)

        payouts = mgr.calculate_payouts(team.team_id, 100.0)
        assert payouts["a"] == 50.0
        assert payouts["b"] == 50.0

    def test_calculate_payouts_weighted(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            "Weighted Team",
            members=[
                {"agent_id": "lead", "role": "lead", "payout_share": 5.0},
                {"agent_id": "helper", "role": "member", "payout_share": 3.0},
                {"agent_id": "junior", "role": "member", "payout_share": 2.0},
            ],
        )
        mgr.activate(team.team_id)

        payouts = mgr.calculate_payouts(team.team_id, 100.0)
        assert payouts["lead"] == 50.0  # 5/10 * 100
        assert payouts["helper"] == 30.0  # 3/10 * 100
        assert payouts["junior"] == 20.0  # 2/10 * 100

    def test_disband(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            "Temp Team",
            members=[{"agent_id": "a", "role": "lead", "payout_share": 1.0}],
        )
        mgr.activate(team.team_id)
        mgr.disband(team.team_id)
        assert team.status == TeamStatus.DISBANDED.value

    def test_get_agent_teams(self, mgr: TeamManager) -> None:
        mgr.form_team("Team Alpha", members=[
            {"agent_id": "agent-x", "role": "lead", "payout_share": 1.0},
        ])
        mgr.form_team("Team Beta", members=[
            {"agent_id": "agent-y", "role": "lead", "payout_share": 0.5},
            {"agent_id": "agent-x", "role": "member", "payout_share": 0.5},
        ])

        x_teams = mgr.get_agent_teams("agent-x")
        assert len(x_teams) == 2

        y_teams = mgr.get_agent_teams("agent-y")
        assert len(y_teams) == 1

    def test_block_task(self, mgr: TeamManager) -> None:
        team = mgr.form_team(
            "Block Team",
            members=[{"agent_id": "a", "role": "lead", "payout_share": 1.0}],
        )
        mgr.activate(team.team_id)
        task = mgr.assign_task(team.team_id, "a", "Something")

        blocked = mgr.block_task(team.team_id, task.task_id, "Waiting for API key")
        assert blocked.status == "blocked"

        progress = mgr.get_team_progress(team.team_id)
        assert progress["blocked"] == 1
