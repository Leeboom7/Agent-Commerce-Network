"""Web API adapter for the hackathon demo."""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from demo.competitive_analysis import run_demo


FALLBACK_QWEN = {
    "plannerOutput": {
        "summary": "Split the buyer request into research, writing, independent verification, and arbitration roles.",
        "workPackages": [
            "collect market evidence and source links",
            "draft the AI vendor risk brief with claim-level citations",
            "verify acceptance criteria against artifacts",
            "resolve failed claims with evidence-backed ruling",
        ],
        "selectedServices": ["market_research", "risk_brief_writing", "claim_verification", "dispute_arbitration"],
    },
    "negotiationRationale": (
        "The buyer accepts specialist agents only after comparing price, reputation, delivery time, "
        "and remedy terms. The writer counteroffer includes a revision and penalty clause because "
        "claim-level verification is required."
    ),
    "arbitrationRationale": (
        "The agreement requires cited factual claims. Verification evidence shows two unsupported claims, "
        "so the ruling upholds the buyer, requires revision, and applies the 10% penalty."
    ),
}


BASELINE = {
    "single_agent": {
        "factual_errors": 4,
        "cost_nc": 320,
        "verified_percent": 0,
    },
    "multi_agent": {
        "factual_errors": 2,
        "cost_nc": 210.33,
        "verified_percent": 100,
    },
    "gain": {
        "fewer_errors_percent": 50,
        "lower_cost_percent": 34,
        "verified_percent": 100,
    },
}


def _build_protocol_events(result: dict[str, Any], qwen: dict[str, Any]) -> list[dict[str, Any]]:
    """Build a judge-readable event stream from the Python demo result."""
    contracts = result.get("contracts", {})
    settlement = result.get("settlement", {})
    arbitration = result.get("arbitration", {})
    verification = result.get("verification_reports", {})

    return [
        {
            "event": "task_request_created",
            "details": "Buyer Agent creates TaskRequest: AI vendor risk brief",
            "data": {"budget": "250 NC", "buyer": "agent-orchestrator-001"},
        },
        {
            "event": "qwen_planner_complete",
            "details": "Qwen planner decomposes task into research, writing, verification, arbitration",
            "data": {"status": qwen.get("status"), "work_packages": qwen.get("plannerOutput", {})},
        },
        {
            "event": "agent_services_matched",
            "details": "Marketplace matches external DataAnalyst, ReportWriter, FactChecker, and Arbitrator runtimes",
            "data": {"runtime_boundary": "external connector runtimes, not platform hosted"},
        },
        {
            "event": "proposal_offer_received",
            "details": "Seller agents submit offers with price, ETA, deliverables, and remedy clauses",
            "data": {
                "data_analyst": contracts.get("data_analyst", {}).get("terms", {}).get("price"),
                "report_writer": contracts.get("report_writer", {}).get("terms", {}).get("price"),
                "fact_checker": contracts.get("fact_checker", {}).get("terms", {}).get("price"),
            },
        },
        {
            "event": "proposal_countered",
            "details": "Buyer counters writer terms with revision requirement and penalty if claim verification fails",
            "data": {"counterparty": "agent-report-writer-001", "penalty_rate": 0.1},
        },
        {
            "event": "agreement_snapshots_created",
            "details": "Accepted proposals become machine-readable Agreements",
            "data": {"agreement_count": len(contracts)},
        },
        {
            "event": "external_runtime_execution",
            "details": "Seller connectors poll paid Agreements and execute in their own runtimes",
            "data": {"hosting": "external", "connector": "REST/OpenAPI adapter loop"},
        },
        {
            "event": "artifact_delivery_submitted",
            "details": "Research and writer runtimes upload artifacts and submit Delivery objects",
            "data": {"artifacts": ["vendor-data.md", "risk-brief.md", "citation-map.json"]},
        },
        {
            "event": "verification_failed_claims",
            "details": "Verifier runtime flags two unsupported claims before buyer acceptance",
            "data": {
                "fact_checker_verdict": verification.get("fact_checker", {}).get("verdict"),
                "failed_claims": 2,
            },
        },
        {
            "event": "dispute_case_opened",
            "details": "Buyer opens DisputeCase with verifier evidence bundle",
            "data": {"evidence": ["failed-claims.md", "verification_report.json"]},
        },
        {
            "event": "arbitration_ruling",
            "details": "Qwen arbitration rationale supports buyer-upheld ruling and remedy",
            "data": {"ruling_type": arbitration.get("ruling_type"), "remedy": arbitration.get("remedy", {})},
        },
        {
            "event": "settlement_complete",
            "details": "Demo ledger pays external agents, applies penalty, and updates reputation",
            "data": {
                "total_cost": settlement.get("total_cost"),
                "payments": settlement.get("payments", []),
                "baseline_gain": BASELINE["gain"],
            },
        },
    ]


async def _build_live_qwen(result: dict[str, Any]) -> dict[str, Any]:
    """Build live Qwen rationale fields when QWEN_API_KEY is available."""
    if not os.getenv("QWEN_API_KEY"):
        return {"status": "fallback", **FALLBACK_QWEN}

    try:
        from acp.llm.qwen import QwenClient

        client = QwenClient()
        settlement = result.get("settlement", {})
        arbitration = result.get("arbitration", {})
        verification = result.get("verification_reports", {})

        planner = await client.chat_structured(
            messages=[
                {
                    "role": "system",
                    "content": "You plan multi-agent commerce workflows. Return concise JSON.",
                },
                {
                    "role": "user",
                    "content": (
                        "Plan the specialist work packages for an AI vendor risk brief. "
                        "Use roles: research, writer, verifier, arbitrator."
                    ),
                },
            ],
            output_schema={
                "summary": "string",
                "workPackages": ["string"],
                "selectedServices": ["string"],
            },
        )
        negotiation = await client.agent_reason(
            system_prompt="You explain autonomous agent negotiation decisions in 2 concise sentences.",
            user_prompt=f"Contracts: {json.dumps(result.get('contracts', {}), default=str)[:2000]}",
        )
        arbitration_reason = await client.agent_reason(
            system_prompt="You explain arbitration decisions using agreement criteria and verifier evidence.",
            user_prompt=(
                f"Verification: {json.dumps(verification, default=str)}\n"
                f"Arbitration: {json.dumps(arbitration, default=str)}\n"
                f"Settlement: {json.dumps(settlement, default=str)}"
            ),
        )
        return {
            "status": "live",
            "plannerOutput": planner,
            "negotiationRationale": negotiation,
            "arbitrationRationale": arbitration_reason,
        }
    except Exception as exc:
        return {
            "status": "fallback",
            "error": str(exc),
            **FALLBACK_QWEN,
        }


async def run_web_demo() -> dict[str, Any]:
    """Run the canonical Python demo and shape it for the Next.js app."""
    result = await run_demo(verbose=False)
    qwen = await _build_live_qwen(result)
    result["qwen"] = qwen
    result["baseline"] = BASELINE
    result["events"] = _build_protocol_events(result, qwen)
    result["runtimeBoundary"] = {
        "hosting": "external",
        "connector": "REST/OpenAPI polling adapter",
        "secrets": "Agent API keys stay in runtime environment variables, never in browser bundles.",
    }
    return result


def main() -> None:
    print(json.dumps(asyncio.run(run_web_demo()), ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
