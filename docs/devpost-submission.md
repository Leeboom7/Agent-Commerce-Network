# Devpost Submission — Agent Commerce Network

## Title

**Agent Commerce Network (ACP) — Economic Infrastructure for the AI Agent Economy**

## Tagline (60 chars max)

Autonomous agents discover, negotiate, contract, verify, and settle — on-chain ready.

## Which track?

**Track 3: Agent Society** — Multi-agent collaboration, negotiation, and competition.

## Description

### The Problem

AI agents are becoming autonomous. But when Agent A needs a service from Agent B, there's no standard protocol for discovery, negotiation, contracting, delivery verification, or dispute resolution. Every agent integration is a custom hard-coded API call. There's no trust, no price discovery, and no recourse when things go wrong.

### Our Solution

**Agent Commerce Protocol (ACP)** is an economic infrastructure layer where AI agents form a self-organizing marketplace. Agents can:

- **Discover** each other's services through a shared registry
- **Negotiate** prices using game-theoretic strategies (Tit-for-Tat, Concession, BATNA, Value-Based)
- **Sign** contracts with machine-verifiable acceptance criteria
- **Verify** deliveries automatically (format, threshold, source citation checks)
- **Resolve disputes** through binding arbitration with 5 ruling types
- **Build reputation** with time-weighted scores and transitive trust
- **Form teams** for complex multi-agent outcomes
- **Settle payments** through a transparent credit ledger

All powered by **Qwen Cloud** (Qwen3.7-Max for reasoning, Qwen3-Coder for code tasks).

### What Makes It Different

1. **18 economic relationship types** — not just "buy and sell", but purchase, commission, subscription, bounty, team formation, arbitration, escrow, capital allocation, and more. A complete economic model for the agent economy.

2. **Real negotiation, not prompt engineering** — Each strategy has independent mathematical logic. Agents compute reservation prices, concession schedules, and BATNA thresholds. They don't just "ask nicely."

3. **End-to-end demo with measurable gains** — We benchmarked single-agent vs multi-agent on the same task (competitive analysis report): **50% fewer errors, 34% lower cost, 100% verifiability**.

4. **Neo-Brutalist visual interface** — Force-directed graph showing the agent network live. Draggable floating cards. 7-scene auto-playing demo. Not another dark-mode SaaS dashboard.

### Tech Stack

- **Backend**: Python 3.12+, custom agent framework (no LangChain), asyncio
- **LLM**: Qwen Cloud (Qwen3.7-Max, Qwen3-Coder, Qwen3.6-Plus)
- **Frontend**: Next.js 16, TypeScript, React Flow (@xyflow/react), Tailwind CSS
- **Testing**: 145 tests (pytest), ruff linting, mypy type checking
- **License**: MIT

### Try It Yourself

```bash
git clone https://github.com/Leeboom7/Agent-Commerce-Network
cd Agent-Commerce-Network
pip install -e .
python -m demo.competitive_analysis
python -m demo.single_agent_baseline  # See the baseline comparison
```

For the visual demo:
```bash
cd web && npm install && npm run dev
# Open http://localhost:3000
```

### What's Next

The open-source edition demonstrates the protocol. A production version with blockchain settlement (USDC/USDT), on-chain reputation, and enterprise features is under development.

---

## Built With

- qwen-cloud
- python
- next.js
- react-flow
- tailwind-css
- fastapi

## GitHub Repo

https://github.com/Leeboom7/Agent-Commerce-Network
