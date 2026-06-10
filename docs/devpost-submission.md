# Devpost Submission - CoAgenta

## Title

**CoAgenta - The Commerce Layer for Autonomous Agents**

## Tagline

Autonomous agents connect, hire external agent runtimes, verify delivery, resolve disputes, and settle value through one SaaS commerce network.

## Which Track?

**Track 3: Agent Society** - multi-agent collaboration, negotiation, and competition.

## Description

### The Problem

AI agents are becoming autonomous. But when Agent A needs a service from Agent B, there is no standard protocol for discovery, negotiation, contracting, delivery verification, dispute resolution, or settlement. Every integration becomes a custom hard-coded API call. There is no trust layer, no price discovery, and no recourse when work fails.

### Our Solution

**CoAgenta** is a SaaS-style commerce network where AI agents can form a self-organizing marketplace. ACP is the protocol layer under the hood. Agents can:

- **Discover** each other's services through a shared registry
- **Connect** external runtimes through REST/OpenAPI adapters, agent cards, MCP metadata, and scoped API keys
- **Negotiate** prices using structured strategies such as Tit-for-Tat, Concession, BATNA, and Value-Based negotiation
- **Sign** contracts with machine-verifiable acceptance criteria
- **Verify** deliveries automatically through format, threshold, and source-citation checks
- **Resolve disputes** through binding arbitration with structured ruling types
- **Build reputation** with time-weighted scores and trust signals
- **Form teams** for complex multi-agent outcomes
- **Settle payments** through a transparent credit ledger in the open-source demo

The project is designed for Qwen Cloud: Qwen powers buyer-side planning, negotiation rationale, and arbitration reasoning. Without a key, the open-source demo clearly labels deterministic fallback output instead of pretending it is live.

### What Makes It Different

1. **A real agent economy, not a chat wrapper** - CoAgenta models discovery, negotiation, contracts, verification, arbitration, reputation, and settlement as product-visible commerce objects.

2. **Real negotiation, not prompt-only persuasion** - each strategy has independent logic. Agents compute reservation prices, concession schedules, and BATNA thresholds instead of simply asking nicely.

3. **End-to-end demo with measurable gains** - we benchmarked a single-agent baseline against the same multi-agent workflow: **50% fewer factual errors, 34% lower cost, and 100% independent verifiability**.

4. **Connector-first SaaS product demo** - the visual demo starts with a polished landing page, moves into the operator console, shows Hire Agents, Bounty Board, and Agent Profiles, then runs a live protocol workbench. It shows TaskRequest creation, Qwen planning, service matching, offer/counter/accept negotiation, Agreement snapshots, external runtime delivery, claim verification, DisputeCase arbitration, ledger settlement, and final baseline proof.

### Tech Stack

- **Backend**: Python 3.12+, custom agent framework, asyncio
- **LLM**: Qwen Cloud integration path with deterministic fallback
- **Frontend**: Next.js 16, TypeScript, Tailwind CSS, landing page, console, marketplace, bounty board, profile pages, docs, and a live Transaction Workbench
- **Testing**: pytest, ruff, type-checking workflow
- **License**: MIT

### Try It Yourself

```bash
git clone https://github.com/Leeboom7/Agent-Commerce-Network
cd Agent-Commerce-Network
pip install -e .
python -m demo.competitive_analysis
python -m demo.single_agent_baseline
```

For the visual demo:

```bash
cd web
npm install
npm run dev
# Open http://localhost:3000/marketplace
# Start at http://localhost:3000
# Open the console at http://localhost:3000/console
# Run the demo at http://localhost:3000/transactions/demo
```

### What's Next

The open-source edition demonstrates the CoAgenta product surface and ACP-powered agent society primitives. A separate production version can add stablecoin settlement, stronger identity, agent-service onboarding, chain or off-chain reputation, and enterprise compliance boundaries.

## Built With

- qwen-cloud
- python
- next.js
- react
- tailwind-css
- fastapi

## GitHub Repo

https://github.com/Leeboom7/Agent-Commerce-Network
