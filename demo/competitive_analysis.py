"""
Demo Scenario: Competitive Analysis Report Generation.

5 specialized agents collaborate through the Agent Commerce Network
to produce a competitive analysis of the 2026 China AI Coding Tools market.

Demonstrates: Discovery → Negotiation → Contract → Delivery →
Verification → Arbitration → Settlement → Reputation

This is the canonical demo for the Qwen Cloud Hackathon (Track 3).
"""

from __future__ import annotations

import asyncio
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Support both `python demo/competitive_analysis.py` and `python -m demo.competitive_analysis`
_here = Path(__file__).resolve().parent.parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

from acp.agent import BaseAgent
from acp.arbitration.arbitrator import ArbitrationEngine
from acp.contract.manager import ContractManager
from acp.negotiation.engine import (
    MarketContext,
    NegotiationEngine,
)
from acp.negotiation.strategies import (
    BATNAStrategy,
    ConcessionStrategy,
    ValueBasedStrategy,
)
from acp.protocol.messaging import reset_message_bus
from acp.protocol.models import (
    ContractTerms,
    PricingModel,
    PricingModelType,
    ServiceContract,
)
from acp.registry.registry import ServiceRegistry
from acp.reputation.ratings import ReputationEngine
from acp.settlement.ledger import TransactionLedger
from acp.verification.verifier import DeliveryVerifier

# --------------------------------------------------------------
# Demo State — shared across all agents
# --------------------------------------------------------------


@dataclass
class DemoState:
    """Shared state for the demo scenario."""
    registry: ServiceRegistry = field(default_factory=ServiceRegistry)
    engine: NegotiationEngine = field(default_factory=NegotiationEngine)
    contract_mgr: ContractManager = field(default_factory=ContractManager)
    verifier: DeliveryVerifier = field(default_factory=DeliveryVerifier)
    reputation: ReputationEngine = field(default_factory=ReputationEngine)
    arbitration: ArbitrationEngine = field(default_factory=ArbitrationEngine)
    ledger: TransactionLedger = field(default_factory=TransactionLedger)
    events: list[dict[str, Any]] = field(default_factory=list)
    agents: dict[str, BaseAgent] = field(default_factory=dict)

    def log(self, event_type: str, details: str, data: dict[str, Any] | None = None) -> None:
        self.events.append({
            "timestamp": datetime.now(UTC).isoformat(),
            "event": event_type,
            "details": details,
            "data": data or {},
        })


# --------------------------------------------------------------
# The Demo Orchestrator
# --------------------------------------------------------------


async def run_demo(verbose: bool = True) -> dict[str, Any]:
    """
    Run the complete competitive analysis demo.

    Returns a dict with all results: contracts, verification reports,
    settlements, reputation updates, and the final report.
    """
    reset_message_bus()
    state = DemoState()

    def say(msg: str) -> None:
        if verbose:
            print(msg)

    # ── Qwen Cloud Integration (optional) ──
    import os
    qwen_available = bool(os.getenv("QWEN_API_KEY"))
    if qwen_available:
        try:
            from acp.llm.qwen import QwenClient
            qwen = QwenClient()
            say("\n[QWEN] Qwen Cloud connected. LLM-powered reasoning enabled.")
        except Exception:
            qwen_available = False
            say("\n[QWEN] API key found but connection failed. Running in simulation mode.")
    else:
        say("\n[QWEN] No QWEN_API_KEY set. Running in deterministic simulation mode.")
        say("[QWEN] Set QWEN_API_KEY to enable LLM-powered agent reasoning.")
        qwen = None

    # ===========================================================
    # SCENE 1: AGENT REGISTRATION
    # ===========================================================
    say("\n" + "=" * 60)
    say("SCENE 1: Agent Registration")
    say("=" * 60)

    # Register specialized agents
    agents_data = [
        ("agent-data-analyst-001", "DataAnalyst-03", "data_analysis",
         "Market data analysis and competitor benchmarking",
         {"languages": ["zh", "en"], "domain": "tech_market"}),
        ("agent-report-writer-001", "ReportWriter-01", "report_writing",
         "Professional report writing with charts and executive summaries",
         {"languages": ["zh", "en"], "formats": ["markdown", "pdf"]}),
        ("agent-fact-checker-001", "FactChecker-01", "fact_checking",
         "Claim verification and source validation",
         {"languages": ["zh", "en"], "tools": ["web_search"]}),
        ("agent-orchestrator-001", "Orchestrator-01", "orchestration",
         "Task decomposition and multi-agent coordination",
         {}),
        ("agent-arbitrator-001", "Arbitrator-01", "arbitration",
         "Automated dispute resolution",
         {}),
    ]

    for agent_id, name, svc_type, desc, caps in agents_data:
        # Register services directly (not via full agent instances)
        from acp.protocol.models import ServiceListing
        listing = ServiceListing(
            agent_id=agent_id,
            service_type=svc_type,
            economic_relationship="purchase",
            title=f"{name} — {svc_type}",
            description=desc,
            capabilities=caps,
            pricing=PricingModel(model_type=PricingModelType.NEGOTIABLE, base_price=50.0),
            tags=[svc_type],
        )
        state.registry.register(listing)
        say(f"  [OK] Registered: {name} ({svc_type})")

    # Set initial reputation
    state.reputation.submit_rating_direct(
        "agent-data-analyst-001", "system", "init",
        {"quality": 4.6, "timeliness": 4.5, "communication": 4.5, "accuracy": 4.8},
    )
    state.reputation.submit_rating_direct(
        "agent-report-writer-001", "system", "init",
        {"quality": 4.4, "timeliness": 4.3, "communication": 4.2, "accuracy": 4.5},
    )
    state.reputation.submit_rating_direct(
        "agent-fact-checker-001", "system", "init",
        {"quality": 4.8, "timeliness": 4.7, "communication": 4.6, "accuracy": 4.9},
    )

    say("\n  Reputation scores initialized:")
    for aid in ["agent-data-analyst-001", "agent-report-writer-001", "agent-fact-checker-001"]:
        rep = state.reputation.get_score(aid)
        say(f"    {aid}: {rep}/100")

    # ===========================================================
    # SCENE 2: DISCOVERY
    # ===========================================================
    say("\n" + "=" * 60)
    say("SCENE 2: Service Discovery")
    say("=" * 60)

    say('\n  Orchestrator: "I need to generate a competitive analysis')
    say('  of the 2026 China AI Coding Tools market."')
    say("\n  Searching registry...")

    data_analysts = state.registry.search(service_type="data_analysis")
    report_writers = state.registry.search(service_type="report_writing")
    fact_checkers = state.registry.search(service_type="fact_checking")

    say(f"  Found: {len(data_analysts)} data analysts, "
        f"{len(report_writers)} report writers, "
        f"{len(fact_checkers)} fact checkers")

    # ===========================================================
    # SCENE 3: NEGOTIATION
    # ===========================================================
    say("\n" + "=" * 60)
    say("SCENE 3: Multi-Agent Negotiation")
    say("=" * 60)

    # Orchestrator (buyer) strategies
    buyer_data = BATNAStrategy(batna_value=60.0, target_price=40.0)
    buyer_report = ConcessionStrategy(reservation_price=90.0, opening_price=50.0)
    buyer_check = BATNAStrategy(batna_value=40.0, target_price=25.0)

    # Service provider (seller) strategies
    seller_data = ConcessionStrategy(reservation_price=30.0, opening_price=70.0)
    seller_report = ConcessionStrategy(reservation_price=60.0, opening_price=120.0)
    seller_check = ValueBasedStrategy(base_price=30.0, value_multiplier=1.0)

    ctx = MarketContext(
        average_price=50.0,
        counterparty_reputation=90.0,
        demand_level=0.6,
        supply_level=0.4,
    )

    # Negotiate with Data Analyst
    session_da = state.engine.start_session(
        "agent-orchestrator-001", "agent-data-analyst-001", "purchase"
    )
    outcome_da = await state.engine.negotiate(
        session_da, buyer_data, seller_data, ctx,
    )
    da_price = outcome_da.agreed_terms.price if outcome_da.agreed_terms else 0
    say(f"\n  Data Analyst negotiation: {outcome_da.outcome_type.value}")
    if outcome_da.agreed_terms:
        say(f"    Agreed price: {da_price:.2f} NC (in {outcome_da.total_rounds} rounds)")

    # Negotiate with Report Writer
    session_rw = state.engine.start_session(
        "agent-orchestrator-001", "agent-report-writer-001", "purchase", max_rounds=20
    )
    outcome_rw = await state.engine.negotiate(
        session_rw, buyer_report, seller_report, ctx,
    )
    rw_price = outcome_rw.agreed_terms.price if outcome_rw.agreed_terms else 0
    say(f"\n  Report Writer negotiation: {outcome_rw.outcome_type.value}")
    if outcome_rw.agreed_terms:
        say(f"    Agreed price: {rw_price:.2f} NC (in {outcome_rw.total_rounds} rounds)")

    # Negotiate with Fact Checker
    session_fc = state.engine.start_session(
        "agent-orchestrator-001", "agent-fact-checker-001", "purchase"
    )
    outcome_fc = await state.engine.negotiate(
        session_fc, buyer_check, seller_check, ctx,
    )
    fc_price = outcome_fc.agreed_terms.price if outcome_fc.agreed_terms else 0
    say(f"\n  Fact Checker negotiation: {outcome_fc.outcome_type.value}")
    if outcome_fc.agreed_terms:
        say(f"    Agreed price: {fc_price:.2f} NC (in {outcome_fc.total_rounds} rounds)")

    state.log("negotiation_complete", "All negotiations finished", {
        "data_analyst_price": da_price,
        "report_writer_price": rw_price,
        "fact_checker_price": fc_price,
    })

    # ── Qwen LLM integration proof ──
    if qwen_available and qwen is not None:
        say("\n  [QWEN] Generating negotiation summary with Qwen3.7-Max...")
        try:
            qwen_summary = await qwen.agent_reason(
                system_prompt=(
                    "You are an economic analyst. Summarize the negotiation outcomes "
                    "between an orchestrator agent and three service agents. "
                    "Keep it to 2-3 sentences."
                ),
                user_prompt=(
                    f"Negotiation results: Data Analyst agreed at {da_price:.2f} NC, "
                    f"Report Writer agreed at {rw_price:.2f} NC, "
                    f"Fact Checker agreed at {fc_price:.2f} NC. "
                    f"These agents will collaborate on a competitive analysis report."
                ),
            )
            say(f"  [QWEN] {qwen_summary.strip()}")
        except Exception:
            say("  [QWEN] LLM call failed, continuing with simulation.")

    # ===========================================================
    # SCENE 4: CONTRACT SIGNING
    # ===========================================================
    say("\n" + "=" * 60)
    say("SCENE 4: Contract Signing")
    say("=" * 60)

    contracts: dict[str, ServiceContract] = {}

    # Data Analyst contract
    c_da = state.contract_mgr.create_contract(
        "agent-orchestrator-001", "agent-data-analyst-001",
        "purchase",
        ContractTerms(
            price=da_price,
            deadline="2026-06-15T00:00:00Z",
            deliverables=["market_data.csv", "competitor_comparison.xlsx"],
            acceptance_criteria=[
                "Must be in CSV format",
                "Must have at least 100 data points",
                "Must cite sources",
            ],
        ),
    )
    state.contract_mgr.sign(c_da.contract_id, "agent-orchestrator-001")
    state.contract_mgr.sign(c_da.contract_id, "agent-data-analyst-001")
    contracts["data_analyst"] = c_da
    say(f"  [OK] Contract {c_da.contract_id}: Data Analyst — {da_price:.2f} NC")

    # Report Writer contract
    c_rw = state.contract_mgr.create_contract(
        "agent-orchestrator-001", "agent-report-writer-001",
        "purchase",
        ContractTerms(
            price=rw_price,
            deadline="2026-06-20T00:00:00Z",
            deliverables=["competitive_analysis_report.md"],
            acceptance_criteria=[
                "Must be in markdown format",
                "Must contain executive summary",
                "Must cite sources",
            ],
            revision_rounds=2,
            penalty_rate=0.10,
        ),
    )
    state.contract_mgr.sign(c_rw.contract_id, "agent-orchestrator-001")
    state.contract_mgr.sign(c_rw.contract_id, "agent-report-writer-001")
    contracts["report_writer"] = c_rw
    say(f"  [OK] Contract {c_rw.contract_id}: Report Writer — {rw_price:.2f} NC")

    # Fact Checker contract
    c_fc = state.contract_mgr.create_contract(
        "agent-orchestrator-001", "agent-fact-checker-001",
        "purchase",
        ContractTerms(
            price=fc_price,
            deadline="2026-06-22T00:00:00Z",
            deliverables=["verification_report.json"],
            acceptance_criteria=[
                "Must be in JSON format",
                "Must cite sources",
            ],
        ),
    )
    state.contract_mgr.sign(c_fc.contract_id, "agent-orchestrator-001")
    state.contract_mgr.sign(c_fc.contract_id, "agent-fact-checker-001")
    contracts["fact_checker"] = c_fc
    say(f"  [OK] Contract {c_fc.contract_id}: Fact Checker — {fc_price:.2f} NC")

    # ===========================================================
    # SCENE 5: DELIVERY & VERIFICATION
    # ===========================================================
    say("\n" + "=" * 60)
    say("SCENE 5: Delivery & Verification")
    say("=" * 60)

    # -- Phase 1: Data Analyst delivers --
    say("\n  --- Phase 1: Data Analyst delivers ---")
    market_data = {
        "data_points": 127,
        "competitors_analyzed": 7,
        "data": [
            {"product": "Claude Code", "market_share_pct": 28, "pricing": "$10-200/mo"},
            {"product": "GitHub Copilot", "market_share_pct": 35, "pricing": "$10-39/mo"},
            {"product": "Cursor", "market_share_pct": 22, "pricing": "$20-40/mo"},
            {"product": "Qwen Code", "market_share_pct": 8, "pricing": "Free-$15/mo"},
            {"product": "TONGYI Lingma", "market_share_pct": 4, "pricing": "Free"},
            {"product": "iFlyCode", "market_share_pct": 2, "pricing": "Free"},
            {"product": "CodeGeeX", "market_share_pct": 1, "pricing": "Free"},
        ],
        "sources": [
            "https://example.com/market-report-2026",
            "https://example.com/devtool-survey",
        ],
    }

    state.contract_mgr.deliver(
        c_da.contract_id, "agent-data-analyst-001", market_data,
    )

    vr_da = state.verifier.verify(
        c_da.contract_id, "agent-orchestrator-001",
        market_data, c_da.terms.acceptance_criteria,
    )
    say(f"    Verification: {vr_da.verdict} ({vr_da.pass_rate*100:.0f}% passed)")

    if vr_da.verdict in ("accepted", "partial"):
        state.contract_mgr.accept(c_da.contract_id, "agent-orchestrator-001")
        state.ledger.transfer(
            "agent-orchestrator-001", "agent-data-analyst-001",
            da_price, c_da.contract_id, "Payment for market data analysis",
        )
        state.reputation.submit_rating_direct(
            "agent-data-analyst-001", "agent-orchestrator-001",
            c_da.contract_id,
            {"quality": 5.0, "timeliness": 5.0, "accuracy": 5.0, "communication": 4.5},
        )
        say(f"    [OK] Accepted. Payment: {da_price:.2f} NC. Reputation updated.")

    # -- Phase 2: Report Writer delivers (with intentional errors) --
    say("\n  --- Phase 2: Report Writer delivers ---")
    draft_report = {
        "report": """# 2026 China AI Coding Tools — Competitive Analysis

## Executive Summary
The China AI coding tools market grew 340% YoY in 2026, reaching $2.1B.

## Market Overview
Claude Code leads with 45% market share according to recent surveys.
GitHub Copilot remains dominant with 35%.

## Key Findings
- Qwen3-Coder was released in March 2026 with 480B parameters.
- Cursor's AI features drove 45% market share growth.
- Local Chinese tools (TONGYI Lingma, iFlyCode) are growing rapidly.

## Sources
- Anthropic Blog
- GitHub Copilot pricing page
- Various market reports
""",
    }

    state.contract_mgr.deliver(
        c_rw.contract_id, "agent-report-writer-001", draft_report,
    )

    vr_rw = state.verifier.verify(
        c_rw.contract_id, "agent-orchestrator-001",
        draft_report, c_rw.terms.acceptance_criteria,
    )
    say(f"    Format verification: {vr_rw.verdict} ({vr_rw.pass_rate*100:.0f}% passed)")

    # -- Phase 3: Fact Checker finds errors --
    say("\n  --- Phase 3: Fact Checker verifies claims ---")
    fact_check_result = {
        "claims_checked": 8,
        "passed": 6,
        "failed": 2,
        "findings": [
            {
                "claim": "Claude Code leads with 45% market share",
                "status": "FAILED",
                "correction": "Source claims 'over 40%', not exactly 45%. Recommend using original wording.",
            },
            {
                "claim": "Qwen3-Coder was released in March 2026",
                "status": "FAILED",
                "correction": "Qwen3-Coder was released April 2, 2026, not March.",
            },
            {
                "claim": "GitHub Copilot remains dominant with 35%",
                "status": "PASSED",
                "source": "GitHub Copilot pricing page",
            },
            {
                "claim": "Cursor's AI features drove 45% market share growth",
                "status": "FAILED",
                "correction": "Same error — 45% is inaccurate. Use 'over 40%'.",
            },
        ],
        "sources_verified": True,
    }

    state.contract_mgr.deliver(
        c_fc.contract_id, "agent-fact-checker-001", fact_check_result,
    )

    vr_fc = state.verifier.verify(
        c_fc.contract_id, "agent-orchestrator-001",
        fact_check_result, c_fc.terms.acceptance_criteria,
    )
    say(f"    Fact check verification: {vr_fc.verdict}")
    say(f"    Found {fact_check_result['failed']} errors in {fact_check_result['claims_checked']} claims")

    if vr_fc.verdict in ("accepted", "partial"):
        state.contract_mgr.accept(c_fc.contract_id, "agent-orchestrator-001")
        state.ledger.transfer(
            "agent-orchestrator-001", "agent-fact-checker-001",
            fc_price, c_fc.contract_id, "Payment for fact checking",
        )
        state.reputation.submit_rating_direct(
            "agent-fact-checker-001", "agent-orchestrator-001",
            c_fc.contract_id,
            {"quality": 5.0, "timeliness": 5.0, "accuracy": 5.0, "communication": 4.8},
        )
        say(f"    [OK] Accepted. Payment: {fc_price:.2f} NC.")

    # ===========================================================
    # SCENE 6: DISPUTE & ARBITRATION
    # ===========================================================
    say("\n" + "=" * 60)
    say("SCENE 6: Dispute & Arbitration")
    say("=" * 60)

    # Orchestrator disputes the report writer's delivery due to errors
    say('\n  Orchestrator: "Report contains factual errors. I dispute this delivery."')

    state.contract_mgr.reject(
        c_rw.contract_id, "agent-orchestrator-001",
        "Report contains 2 factual errors identified by Fact Checker",
    )

    # Create a verification report for the dispute from the fact checker's findings
    from acp.protocol.models import CheckResult, VerificationReport
    dispute_vr = VerificationReport(
        contract_id=c_rw.contract_id,
        verifier_id="agent-fact-checker-001",
        checks=[
            CheckResult(
                criterion="Accuracy: market share data",
                passed=False,
                actual_value="45%",
                expected_value="over 40%",
                notes="Rounding error — claim is overstated",
            ),
            CheckResult(
                criterion="Accuracy: Qwen3-Coder release date",
                passed=False,
                actual_value="March 2026",
                expected_value="April 2, 2026",
                notes="Incorrect month",
            ),
            CheckResult(
                criterion="Must be in markdown format",
                passed=True,
            ),
        ],
        verdict="partial",
        summary="2 of 3 accuracy checks failed. Report needs revision.",
    )

    # File arbitration with verification evidence
    case = state.arbitration.file_case(
        contract=c_rw,
        claimant_id="agent-orchestrator-001",
        claim=(
            "Report contains factual errors: incorrect market share data "
            "and wrong release date. Delivery does not meet acceptance criteria."
        ),
        evidence={
            "fact_check_report": fact_check_result,
            "original_claims_with_errors": [
                "Claude Code leads with 45% market share (actual: 'over 40%')",
                "Qwen3-Coder released March 2026 (actual: April 2, 2026)",
            ],
        },
        verification_report=dispute_vr,
    )
    say(f"  Case filed: {case.case_id}")

    # Rule
    ruling = state.arbitration.rule(
        case_id=case.case_id,
        arbitrator_id="agent-arbitrator-001",
        contract=c_rw,
    )
    say(f"\n  Ruling: {ruling.ruling_type.value}")
    say(f"  Reasoning: {ruling.reasoning}")
    say(f"  Remedy: {ruling.remedy['action']}")

    # Enforce ruling — seller revises
    say('\n  Report Writer: "Understood. I will revise the report with corrected data."')

    # Simulate revision
    revised_report = {
        "report": draft_report["report"]
        .replace("45% market share", "over 40% market share")
        .replace("March 2026", "April 2, 2026"),
    }

    state.contract_mgr.deliver(
        c_rw.contract_id, "agent-report-writer-001", revised_report,
    )

    # Re-verify
    vr_rw2 = state.verifier.verify(
        c_rw.contract_id, "agent-orchestrator-001",
        revised_report, c_rw.terms.acceptance_criteria,
    )
    say(f"  Revised verification: {vr_rw2.verdict}")

    # Accept the revised delivery
    state.contract_mgr.accept(c_rw.contract_id, "agent-orchestrator-001")

    # Apply penalty: 10% deduction
    penalty_amount = rw_price * 0.10
    net_payment = rw_price - penalty_amount
    state.ledger.transfer(
        "agent-orchestrator-001", "agent-report-writer-001",
        net_payment, c_rw.contract_id,
        f"Payment with {penalty_amount:.2f} NC penalty for errors",
    )
    state.reputation.submit_rating_direct(
        "agent-report-writer-001", "agent-orchestrator-001",
        c_rw.contract_id,
        {"quality": 3.5, "timeliness": 4.0, "accuracy": 3.0, "communication": 4.5},
    )
    say(f"    [OK] Accepted with penalty. Payment: {net_payment:.2f} NC (penalty: {penalty_amount:.2f} NC)")

    # ===========================================================
    # SCENE 7: SETTLEMENT & REPUTATION
    # ===========================================================
    say("\n" + "=" * 60)
    say("SCENE 7: Settlement & Reputation Summary")
    say("=" * 60)

    say("\n  Transaction Ledger:")
    say(f"  {'From':<25} {'To':<25} {'Amount':>8} {'Reason'}")
    say(f"  {'-'*25} {'-'*25} {'-'*8} {'-'*30}")
    for txn in state.ledger.get_history():
        say(f"  {txn['from_agent']:<25} {txn['to_agent']:<25} {txn['amount']:>8.2f} {txn['reason'][:30]}")

    say("\n  Reputation Scores:")
    for aid in ["agent-data-analyst-001", "agent-report-writer-001", "agent-fact-checker-001"]:
        rep = state.reputation.get_reputation(aid)
        say(f"    {aid}: {rep.composite_score:.1f}/100 "
            f"({rep.total_transactions} txns, {rep.success_rate*100:.0f}% success)")

    say(f"\n  Orchestrator Balance: {state.ledger.get_balance('agent-orchestrator-001'):.2f} NC")

    total_cost = da_price + net_payment + fc_price
    say(f"  Total Project Cost: {total_cost:.2f} NC")

    # ===========================================================
    # RETURN RESULTS
    # ===========================================================
    say("\n" + "=" * 60)
    say("DEMO COMPLETE")
    say("=" * 60)

    return {
        "contracts": {k: c.to_dict() for k, c in contracts.items()},
        "verification_reports": {
            "data_analyst": {"verdict": vr_da.verdict, "pass_rate": vr_da.pass_rate},
            "report_writer_initial": {"verdict": vr_rw.verdict, "pass_rate": vr_rw.pass_rate},
            "report_writer_revised": {"verdict": vr_rw2.verdict, "pass_rate": vr_rw2.pass_rate},
            "fact_checker": {"verdict": vr_fc.verdict, "pass_rate": vr_fc.pass_rate},
        },
        "arbitration": {
            "case_id": case.case_id,
            "ruling_type": ruling.ruling_type.value,
            "remedy": ruling.remedy,
        },
        "settlement": {
            "total_cost": total_cost,
            "payments": [
                {"agent": "agent-data-analyst-001", "amount": da_price, "penalty": 0},
                {"agent": "agent-report-writer-001", "amount": net_payment, "penalty": penalty_amount},
                {"agent": "agent-fact-checker-001", "amount": fc_price, "penalty": 0},
            ],
        },
        "reputation": {
            aid: {
                "score": state.reputation.get_score(aid),
                "transactions": state.reputation.get_reputation(aid).total_transactions,
                "success_rate": state.reputation.get_reputation(aid).success_rate,
            }
            for aid in [
                "agent-data-analyst-001",
                "agent-report-writer-001",
                "agent-fact-checker-001",
            ]
        },
        "events": state.events,
    }


# --------------------------------------------------------------
# Entry Point
# --------------------------------------------------------------

if __name__ == "__main__":
    result = asyncio.run(run_demo(verbose=True))
    print("\nFinal Result Summary:")
    print(f"  Contracts signed: {len(result['contracts'])}")
    print(f"  Total cost: {result['settlement']['total_cost']:.2f} NC")
    print(f"  Arbitration ruling: {result['arbitration']['ruling_type']}")
