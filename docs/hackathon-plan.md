# CoAgenta Hackathon Plan

## Context

- **Hackathon**: Qwen Cloud Global AI Hackathon
- **Track**: Track 3, Agent Society
- **Deadline**: July 9, 2026
- **Primary goal**: Win the hackathon
- **Secondary goal**: Build GitHub open-source influence

The project is now positioned as **CoAgenta**, a SaaS-style Agent commerce console. ACP remains the underlying protocol layer, but the demo should not feel like a protocol spec viewer.

## Winning Narrative

Most Agent demos show agents as tools that answer humans. CoAgenta shows agents as economic participants:

```text
external agents connect -> list services -> discover work -> negotiate
-> sign agreements -> deliver artifacts -> get verified
-> resolve disputes -> settle credits -> update reputation
```

The hackathon story must make three points quickly:

1. **Agent society needs economic infrastructure**, not only multi-agent chat.
2. **CoAgenta is the operator console** for that network.
3. **ACP powers the transaction mechanics** under the product.

## Product Architecture

```text
CoAgenta Web App
  Landing | Console | Hire Agents | Bounty Board | Docs | Transaction Workbench
        |
Next.js API Bridge
        |
Python Demo / ACP SDK
        |
Commerce Core
  Registry | Negotiation | Contract | Verification
  Reputation | Arbitration | Settlement | Team
        |
External Agent Runtimes
  MCP tools | REST/OpenAPI | Agent cards | local scripts | containers
        |
Qwen Cloud Decision Layer
```

## Demo Path

Use this sequence for judging and video:

1. `/` - Landing page explains the product, marketplace, bounty board, and scroll-driven commerce loop.
2. `/console` - Console shows My Agents, active deals, connector health, recent protocol events.
3. `/marketplace` - Hire Agents shows discoverable external AgentServices.
4. `/bounties` - Bounty Board shows work packages agents can bid on.
5. `/agents/dataanalyst-03` - Agent economic identity page.
6. `/transactions/demo` - Run the live transaction workbench.

The transaction demo must show:

- Qwen planner/rationale layer, with fallback when `QWEN_API_KEY` is missing.
- AgentService discovery.
- Multi-round negotiation.
- Contract signing.
- Artifact delivery.
- Verification failure.
- Dispute and arbitration.
- NC credit settlement.
- Reputation update.
- Baseline comparison.

## Technical Stack

| Layer | Technology |
| --- | --- |
| Product UI | Next.js 16.2.7, React 19.2.4, TypeScript 5, Tailwind CSS 4 |
| Protocol/demo | Python 3.12+ |
| LLM | Qwen Cloud via OpenAI-compatible client, optional fallback |
| Agent runtime model | External runtimes via connectors, not platform-hosted execution |
| API bridge | Next.js route spawning `python -m demo.web_api` |
| Tests | pytest, ruff, mypy where installed, ESLint, Next build |
| Deployment target | Alibaba Cloud / Next.js compatible runtime |

## Current MVP Scope

Implemented or in demo scope:

- In-memory ServiceRegistry.
- Negotiation engine and strategy classes.
- Contract manager and lifecycle states.
- Delivery verifier.
- Reputation engine and trust graph.
- Arbitration engine.
- NC credit ledger.
- Team manager.
- Qwen wrapper with fallback.
- Next.js CoAgenta Console, Hire Agents, Bounty Board, Docs, Agent Profile, Transaction Workbench.

Explicitly out of scope for hackathon MVP:

- Real user auth and multi-tenant org permissions.
- Real escrow, blockchain settlement, KYC/AML, production compliance.
- Persistent database migration.
- Fully hosted agent runtime marketplace.
- Real MCP server publishing flow.

## Submission Priorities

### Must Ship

- CoAgenta-first README and docs.
- Working landing page.
- Working Console at `/console`.
- Working Hire Agents and Bounty Board.
- Working transaction workbench.
- Reliable fallback path without `QWEN_API_KEY`.
- Demo video under 3 minutes.
- Clear Devpost copy explaining Agent society and Qwen role.

### Should Ship

- Alibaba Cloud deployment path.
- Cleaner architecture diagram reflecting CoAgenta + ACP.
- English README parity with README_CN.
- Recorded proof that lint/build pass.

### Could Ship

- More realistic connector examples.
- Better visual polish for mobile.
- Additional bounties and agent profiles.
- Docs for adding a new verifier or negotiation strategy.

## Quality Gate

Before submission:

```bash
pytest tests/ -q
ruff check acp/ tests/ demo/
python -m mypy acp/ --ignore-missing-imports

cd web
npm run lint
npm run build
```

Known caveat: Python static checks may already have pre-existing ruff/mypy environment issues. Do not hide them; document actual status.

## Naming Rules

- Use `CoAgenta` for product, site, app, and GitHub-facing project narrative.
- Use `ACP` only for the underlying protocol and Python primitives.
- Avoid `AgentVerse` as the primary name because it sounds metaverse-like and collides with existing names.
- Do not reintroduce `Agent Commerce Network` as the main product name unless the whole brand strategy changes again.
