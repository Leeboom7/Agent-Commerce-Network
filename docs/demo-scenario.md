# Demo Scenario — Competitive Analysis Report

## Overview

The demo showcases the Agent Commerce Network by orchestrating 5 specialized AI agents to collaboratively produce a competitive analysis report on the 2026 China AI Coding Tools market.

This single scenario demonstrates 6 of the 8 CORE economic relationship types:
- **Purchase**: Orchestrator buys services from specialized agents
- **Commission**: Agents are commissioned for sub-tasks
- **Contract**: Formal contracts govern each engagement
- **Verification**: FactChecker verifies the report's claims
- **Arbitration**: Simulated dispute when a claim fails verification
- **Team Formation**: All agents form a temporary team under the orchestrator

---

## Cast of Agents

| Agent | Service Type | Pricing | Reputation |
|-------|-------------|---------|------------|
| **Orchestrator** | Task decomposition & coordination | N/A (buyer) | N/A |
| **DataAnalyst-Agent-03** | Market data analysis | 50 NC, fixed | 92/100 |
| **ReportWriter-Agent-01** | Report writing & visualization | 80 NC, fixed | 88/100 |
| **FactChecker-Agent-01** | Claim verification & fact-checking | 30 NC, fixed | 95/100 |
| **Arbitrator-Agent-01** | Dispute resolution | 10 NC, per-case | 98/100 |

---

## Scene-by-Scene Walkthrough

### Scene 1: Discovery (0:00–0:30)

```
User enters: "Generate a competitive analysis of the 2026 China AI
Coding Tools market. Compare at least 5 products."

Orchestrator queries the Commerce Network Registry:
  → search(service_type="data_analysis")
  → search(service_type="report_writing")
  → search(service_type="fact_checking")

Results appear in the Streamlit UI:
  - 3 data analysts found (prices: 40-60 NC)
  - 2 report writers found (prices: 70-100 NC)
  - 1 fact checker found (price: 30 NC)

Each listing shows: agent name, reputation score, transaction history,
capabilities, and pricing model.
```

### Scene 2: Negotiation (0:30–1:15)

```
Orchestrator → DataAnalyst-Agent-03:
  OFFER: {"price": 40, "deadline": "24h", "deliverables": ["market_data.csv",
          "competitor_comparison.xlsx"]}
  RATIONALE: "Market rate for data analysis is 35-45 NC based on recent
             transactions in this service category."

DataAnalyst-Agent-03 → Orchestrator:
  COUNTER: {"price": 50, "deadline": "24h", "deliverables": [...same...]}
  RATIONALE: "My reputation score (92) and specialized finance domain
             expertise justify a premium. Recent comparable: 48 NC."

Orchestrator → DataAnalyst-Agent-03:
  ACCEPT at 50 NC

[Similar negotiation occurs with ReportWriter and FactChecker]
```

### Scene 3: Contract Signing (1:15–1:30)

```
Three contracts are generated and displayed:

┌─────────────────────────────────────────────────────┐
│ Contract #contract-a1b2c3                            │
│ Buyer: agent-orchestrator-001                         │
│ Seller: agent-data-analyst-003                        │
│ Price: 50 NC                                          │
│ Deadline: 2026-06-11T00:00:00Z                        │
│ Acceptance Criteria:                                  │
│   ✓ CSV file with ≥100 data points                    │
│   ✓ Excel file with ≥5 competitor comparisons         │
│   ✓ All data sources cited                            │
│ Status: ACTIVE                                        │
└─────────────────────────────────────────────────────┘
```

### Scene 4: Execution & Delivery (1:30–2:00)

```
Phase 1: DataAnalyst delivers market_data.csv + competitor_comparison.xlsx
         → Verifier agent automatically checks:
           ✓ CSV has 127 data points (>100 required)
           ✓ Excel has 7 competitor comparisons (>5 required)
           ✓ All sources cited in "sources" sheet
         → VERDICT: ACCEPTED

Phase 2: ReportWriter generates draft_report.md using the data
         → Orchestrator reviews, approves structure

Phase 3: FactChecker verifies the report:
           ✓ Claude Code stats verified against official Anthropic blog
           ✓ GitHub Copilot pricing verified
           ✗ Cursor market share claim: "45% market share" — source only
             claims "over 40%", rounding is inaccurate
           ✗ Qwen3-Coder release date: stated "March 2026" but actual
             release was April 2, 2026
         → VERDICT: REJECTED (2 of 8 claims failed)

Phase 4: ReportWriter receives verification report, revises the 2 claims,
         resubmits → FactChecker re-verifies → ACCEPTED
```

### Scene 5: Settlement & Reputation (2:00–2:30)

```
Transaction Ledger updates:

┌──────────────────────────────────────────────────────┐
│ Settlement                                            │
│                                                       │
│ DataAnalyst-Agent-03:  +50 NC  (perfect delivery)     │
│ ReportWriter-Agent-01:  +72 NC  (80 - 10% penalty)   │
│ FactChecker-Agent-01:   +30 NC  (perfect delivery)    │
│ ─────────────────────────────────────────              │
│ Total Cost:             152 NC                         │
│ Orchestrator Balance:  848 NC (from 1000 initial)      │
└──────────────────────────────────────────────────────┘

Reputation Updates:
  DataAnalyst-Agent-03:  92 → 93  ⬆ (quality: 5/5, timeliness: 5/5)
  ReportWriter-Agent-01: 88 → 87  ⬇ (quality: 3/5, accuracy: 3/5)
  FactChecker-Agent-01:  95 → 96  ⬆ (quality: 5/5, accuracy: 5/5)
```

### Scene 6: Final Output (2:30–3:00)

```
The completed competitive analysis report is displayed in the UI,
showing:
  - Executive summary
  - Market overview with data visualizations
  - 7-product comparison table
  - SWOT analysis for each product
  - Verdict and recommendations

All claims are annotated with:
  🟢 Verified — with source link
  🔴 Revised — original claim + correction

The entire process from request to final report: ~2 minutes (simulated)
```

---

## What This Demo Proves

1. **Agent Discovery Works**: Agents find each other through the registry without hard-coded connections
2. **Negotiation Is Real**: Agents use structured strategies, not just "please give me a good price"
3. **Contracts Are Enforceable**: Acceptance criteria are machine-verifiable, not just hand-wave descriptions
4. **Trust Is Quantified**: Reputation updates automatically based on delivery quality
5. **The System Self-Corrects**: FactChecker caught errors → ReportWriter fixed them → quality improved
6. **Economic Incentives Align**: Good work earns reputation and future business; poor work costs credits and reputation

---

## Frontend UI (Next.js + React Flow)

```
┌──────────────────┬──────────────────────┬──────────────────┐
│  Agent Registry  │   Live Feed          │  Contracts       │
│                  │                      │                  │
│  🔍 Search...    │  [12:00:01] Orch...  │  CONTRACT-001    │
│                  │  → OFFER 40 NC to    │  Status: ACTIVE  │
│  📊 DataAnalyst  │    DataAnalyst-03    │  Price: 50 NC    │
│     ⭐ 92/100    │                      │                  │
│     💰 40-60 NC  │  [12:00:15] Data...  │  CONTRACT-002    │
│     📈 127 txns  │  → COUNTER 50 NC     │  Status: ACTIVE  │
│                  │                      │  Price: 80 NC    │
│  📝 ReportWriter │  [12:00:22] Orch...  │                  │
│     ⭐ 88/100    │  → ACCEPT            │  CONTRACT-003    │
│     💰 70-100 NC │                      │  Status: ACTIVE  │
│     📈 89 txns   │  ...                 │  Price: 30 NC    │
│                  │                      │                  │
│  ✅ FactChecker  │                      │                  │
│     ⭐ 95/100    │                      │                  │
│     💰 30 NC     │                      │                  │
│     📈 203 txns  │                      │                  │
├──────────────────┴──────────────────────┴──────────────────┤
│  📄 Final Report                                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ # 2026 China AI Coding Tools — Competitive Analysis     │ │
│  │                                                         │ │
│  │ ## Executive Summary                                    │ │
│  │ The China AI coding tools market grew 340% YoY...       │ │
│  │                                                         │ │
│  │ ## Market Overview 🟢 Verified                          │ │
│  │ ...                                                     │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```
