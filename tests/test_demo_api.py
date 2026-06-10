"""Tests for the web-facing demo API wrapper."""

from __future__ import annotations

import asyncio

from demo.web_api import run_web_demo


def test_run_web_demo_returns_qwen_contract() -> None:
    result = asyncio.run(run_web_demo())

    assert result["qwen"]["status"] in {"fallback", "live"}
    assert result["qwen"]["plannerOutput"]
    assert result["qwen"]["negotiationRationale"]
    assert result["qwen"]["arbitrationRationale"]
    assert len(result["events"]) >= 10
    event_names = {event["event"] for event in result["events"]}
    assert "qwen_planner_complete" in event_names
    assert "proposal_countered" in event_names
    assert "verification_failed_claims" in event_names
    assert "arbitration_ruling" in event_names
    assert "settlement_complete" in event_names
    assert len(result["contracts"]) == 3
    assert result["settlement"]["total_cost"] > 0
    assert result["baseline"]["multi_agent"]["verified_percent"] == 100
