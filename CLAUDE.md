# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Identity

CoAgenta is a SaaS-style commerce network for autonomous AI agents. It's a monorepo with a Python ACP (Agent Commerce Protocol) SDK and a Next.js web app. Unlike LangChain/CrewAI/AutoGen (which focus on how agents execute tasks), CoAgenta focuses on how agents transact: discovery, negotiation, contracts, delivery, verification, dispute resolution, settlement, and reputation.

**Branding**: The product is "CoAgenta". ACP is the underlying protocol layer, referenced only as "Powered by ACP" or in dev docs. External agent connections are "Connectors".

**Priority**: Hackathon demo (Qwen Cloud Global AI Hackathon Track 3: Agent Society) first, open-source impact second.

See `AGENTS.md` for detailed engineering constraints, brand rules, and known quality limitations.

## Build / Lint / Test

### Python (root)

```bash
pip install -e ".[dev]"          # includes pytest, ruff, mypy
pip install -e ".[demo]"         # adds streamlit, plotly

pytest tests/ -q                  # run all tests (~146 passed, 10 skipped)
pytest tests/test_negotiation.py -v  # run a single test file

ruff check acp/ tests/ demo/     # lint (line-length 110, py312)
mypy acp/ --ignore-missing-imports  # type check

python -m demo.competitive_analysis    # canonical demo
python -m demo.single_agent_baseline   # single-agent baseline comparison
```

### Web (Next.js)

```bash
cd web
npm install
npm run dev         # http://localhost:3000
npm run lint        # eslint
npm run build       # production build
```

### CI

CI runs on push/PR to `main`: Python 3.12 + 3.13 (ruff → mypy → pytest → demo CLI smoke tests) and Node 20 (lint → build). See `.github/workflows/ci.yml`.

### Web env vars for demo bridge

The Next.js API bridge (`POST /api/demo/run`) spawns `python -m demo.web_api`. Set these in the web directory:

```bash
PYTHON_BIN=python
ACN_DEMO_REPO_ROOT=..
QWEN_API_KEY=your-key-here   # optional; missing → deterministic fallback
```

`QWEN_API_KEY` must stay server-side only — never in browser bundles.

## Architecture

```
Web App (Next.js 16 + React 19 + Tailwind 4 + TypeScript 5)
  Landing | Console | Hire Agents | Bounty Board | Docs | Transaction Workbench
        |
POST /api/demo/run → spawns python -m demo.web_api → JSON
        |
Python Demo / ACP SDK
        |
acp/protocol/     — types, dataclass models, message bus
acp/registry/     — service registration & discovery
acp/negotiation/  — NegotiationEngine + strategy classes
acp/contract/     — ContractManager + state transitions
acp/verification/ — DeliveryVerifier (heuristic, not LLM-dependent)
acp/reputation/   — ReputationEngine + TrustGraph
acp/arbitration/  — ArbitrationEngine
acp/settlement/   — TransactionLedger
acp/team/         — TeamManager
acp/relationships/ — composes primitives into purchase, commission, contract,
                     subscription, bounty, team formation, verification, arbitration
acp/llm/          — QwenClient (Qwen Cloud, OpenAI-compatible API)
demo/             — CLI demos, Streamlit app, web_api.py bridge
```

Key navigation paths (top bar): Console (`/console`), Hire Agents (`/marketplace`), Bounty Board (`/bounties`), Docs (`/docs`).

## Key Files

| File | Purpose |
|------|---------|
| `web/src/components/app-header.tsx` | Top nav with the four main entries |
| `web/src/lib/demo-catalog.ts` | Static frontend data: agents, services, bounties, metrics |
| `web/src/app/page.tsx` | Public landing page |
| `web/src/app/console/page.tsx` | Operator console |
| `web/src/app/marketplace/page.tsx` | Hire Agents |
| `web/src/app/bounties/page.tsx` | Bounty Board |
| `web/src/app/agents/[slug]/page.tsx` | Agent economic identity page |
| `web/src/app/transactions/demo/transaction-workbench.tsx` | Live transaction workbench (hackathon centerpiece) |
| `web/src/app/api/demo/run/route.ts` | Next.js → Python bridge |
| `web/src/app/globals.css` | Global styles — large file, scope changes carefully |
| `demo/web_api.py` | Python adapter that builds judge-readable protocol event stream |
| `demo/competitive_analysis.py` | Canonical multi-agent demo |

## Extension Rules

- **New relationship types**: Combine existing primitives in `acp/relationships/` rather than copying entire transaction flows. Add tests covering success, failure, and state transitions.
- **New negotiation strategies**: Subclass `BaseNegotiationStrategy`, register in `create_strategy()`. Test initial offer, accept, counter, reject/withdraw.
- **New verifiers**: Deterministic tests first; LLM may only augment, never be the sole verification path.
- **Frontend changes**: Keep the four top-level nav entries concise. Before large `globals.css` edits, check existing theater/workbench selectors. `/` must show real product boxes, not empty marketing hero. `/console` is a SaaS cockpit — evidence over decorative animations.
- **Persistence/backend additions**: Define idempotency, transaction boundaries, concurrency, audit logging before implementation. Keep the existing public API stable.

## Known Limitations (MVP)

- In-memory only: registry, contracts, ledger, reputation, arbitration cases — not production-persistent.
- `DeliveryVerifier` is heuristic; fuzzy criteria may default to pass.
- `ContractManager.sign()` uses MVP `_signatures` dict, not cryptographic signatures.
- `ReputationEngine.submit_rating()` doesn't auto-infer rated agent from transaction ID.
- `NegotiationEngine` `max_sessions` is not enforced.
- No real escrow, on-chain settlement, KYC, or production security/auth.
