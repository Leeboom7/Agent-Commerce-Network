"""
Streamlit Demo — Agent Commerce Network.

Interactive visualization of the Agent Commerce Protocol.
Shows the complete lifecycle: Discovery → Negotiation → Contract →
Delivery → Verification → Arbitration → Settlement → Reputation.

Run: streamlit run demo/app.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Ensure acp is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd

from demo.competitive_analysis import run_demo


st.set_page_config(
    page_title="Agent Commerce Network Demo",
    page_icon="[acp]",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Sidebar ────────────────────────────────────────────────

with st.sidebar:
    st.title("ACP Demo")
    st.markdown("---")
    st.markdown("""
    **Agent Commerce Protocol (ACP)** is an economic infrastructure
    layer where AI agents discover, negotiate, contract, verify,
    and settle transactions autonomously.

    This demo shows 5 agents collaborating on a competitive
    analysis report through the full commerce lifecycle.
    """)

    st.markdown("---")
    st.markdown("### Economic Relationship Types")
    st.markdown("""
    - Purchase
    - Commission
    - Contract
    - Subscription
    - Open Bounty
    - Team Formation
    - Verification
    - Arbitration
    """)

    st.markdown("---")
    st.markdown("### Tech Stack")
    st.markdown("""
    - Python 3.12+
    - Qwen Cloud (LLM backend)
    - Custom agent framework
    - SQLite (ledger)
    - Streamlit (UI)
    """)

    st.markdown("---")
    st.markdown("*Qwen Cloud Hackathon — Track 3: Agent Society*")


# ── Main Page ───────────────────────────────────────────────

st.title("Agent Commerce Network")
st.caption("Multi-Agent Economic Infrastructure Demo — Competitive Analysis Report")

# Run demo button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_clicked = st.button(
        "Run Demo Scenario",
        type="primary",
        use_container_width=True,
    )

if "demo_result" not in st.session_state:
    st.session_state.demo_result = None
if "demo_events" not in st.session_state:
    st.session_state.demo_events = []

if run_clicked:
    with st.spinner("Running demo scenario... Agents negotiating..."):
        result = asyncio.run(run_demo(verbose=False))
        st.session_state.demo_result = result
        st.session_state.demo_events = result.get("events", [])
    st.success("Demo complete!")
    st.rerun()

result = st.session_state.demo_result

if result is None:
    st.info("Click 'Run Demo Scenario' to start the multi-agent commerce simulation.")
    st.markdown("""
    ### What you'll see:

    1. **Agent Registration** — 5 specialized agents register services
    2. **Service Discovery** — Orchestrator searches for data analysts, report writers, fact checkers
    3. **Multi-Agent Negotiation** — 3 bilateral negotiations with different strategies
    4. **Contract Signing** — Structured contracts with acceptance criteria
    5. **Delivery & Verification** — Automated acceptance checking
    6. **Dispute & Arbitration** — Factual errors found → dispute → ruling → revision
    7. **Settlement & Reputation** — Payments, penalties, and reputation updates
    """)
else:
    # ═══════════════════════════════════════════════════════
    # Tab 1: Contracts
    # ═══════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Contracts", "Verification", "Arbitration",
        "Settlement", "Reputation",
    ])

    with tab1:
        st.subheader("Signed Contracts")
        contracts = result["contracts"]
        if contracts:
            df = pd.DataFrame([
                {
                    "Contract ID": cid[:16] + "...",
                    "Relationship": c.get("relationship_type", "purchase"),
                    "Price (NC)": c["terms"]["price"],
                    "Status": c["status"],
                }
                for cid, c in contracts.items()
            ])
            st.dataframe(df, use_container_width=True)

            for name, contract in contracts.items():
                with st.expander(f"{name} — {contract['terms']['price']} NC"):
                    st.json(contract)

    # ═══════════════════════════════════════════════════════
    # Tab 2: Verification
    # ═══════════════════════════════════════════════════════
    with tab2:
        st.subheader("Verification Reports")
        vr = result.get("verification_reports", {})
        if vr:
            df = pd.DataFrame([
                {"Delivery": name, "Verdict": v["verdict"], "Pass Rate": f"{v['pass_rate']*100:.0f}%"}
                for name, v in vr.items()
            ])
            st.dataframe(df, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            items = list(vr.items())
            for i, (name, v) in enumerate(items):
                with [col1, col2, col3][i % 3]:
                    color = "green" if v["verdict"] == "accepted" else (
                        "orange" if v["verdict"] == "partial" else "red"
                    )
                    st.metric(
                        name.replace("_", " ").title(),
                        v["verdict"].upper(),
                        delta=f"{v['pass_rate']*100:.0f}% pass",
                        delta_color="normal" if v["verdict"] == "accepted" else "off",
                    )

    # ═══════════════════════════════════════════════════════
    # Tab 3: Arbitration
    # ═══════════════════════════════════════════════════════
    with tab3:
        st.subheader("Arbitration Ruling")
        arb = result.get("arbitration", {})
        if arb:
            st.markdown(f"**Case ID:** `{arb['case_id']}`")
            st.markdown(f"**Ruling:** {arb['ruling_type'].replace('_', ' ').upper()}")
            st.markdown(f"**Remedy:** {arb['remedy']['action'].replace('_', ' ').title()}")

            if arb["remedy"].get("penalty_to_seller"):
                st.warning(f"Penalty applied to seller: {arb['remedy']['penalty_to_seller']*100:.0f}%")

    # ═══════════════════════════════════════════════════════
    # Tab 4: Settlement
    # ═══════════════════════════════════════════════════════
    with tab4:
        st.subheader("Transaction Ledger")
        settlement = result.get("settlement", {})
        payments = settlement.get("payments", [])

        if payments:
            df = pd.DataFrame([
                {
                    "Agent": p["agent"],
                    "Amount (NC)": p["amount"],
                    "Penalty (NC)": p["penalty"],
                    "Net (NC)": p["amount"] - p["penalty"],
                }
                for p in payments
            ])
            st.dataframe(df, use_container_width=True)

            st.metric("Total Project Cost", f"{settlement.get('total_cost', 0):.2f} NC")

    # ═══════════════════════════════════════════════════════
    # Tab 5: Reputation
    # ═══════════════════════════════════════════════════════
    with tab5:
        st.subheader("Reputation Scores")
        rep = result.get("reputation", {})
        if rep:
            df = pd.DataFrame([
                {
                    "Agent": aid[:25] + "...",
                    "Score": f"{r['score']:.1f}/100",
                    "Transactions": r["transactions"],
                    "Success Rate": f"{r['success_rate']*100:.0f}%",
                }
                for aid, r in rep.items()
            ])
            st.dataframe(df, use_container_width=True)

            # Bar chart
            chart_data = pd.DataFrame({
                "Agent": [aid.split("-")[2][:8] for aid in rep],
                "Score": [r["score"] for r in rep.values()],
            })
            st.bar_chart(chart_data.set_index("Agent"))

    # ═══════════════════════════════════════════════════════
    # Footer
    # ═══════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown(
        "*Built for the Qwen Cloud Global AI Hackathon (Track 3: Agent Society). "
        "Agent Commerce Protocol v0.1.0 — MIT License.*"
    )
