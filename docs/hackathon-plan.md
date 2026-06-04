# Agent Commerce Network — Hackathon Development Plan

## Context

- **Hackathon**: Qwen Cloud Global AI Hackathon (Track 3: Agent Society)
- **Deadline**: July 9, 2026
- **Duration**: 5 weeks (June 4 – July 8)
- **Prize Pool**: $70,000+ ($7,000 per track winner)
- **Requirements**: Use Qwen Cloud models, open-source code, Alibaba Cloud deployment

## Architecture

See `docs/architecture.svg` for the visual architecture diagram.

```
┌─────────────────────────────────────────────────────────┐
│                  Agent Commerce Network (ACP)             │
│                                                          │
│  Agent Layer: Buyer | Seller | Arbitrator | Verifier     │
│  SDK/Protocol: Identity, Messaging, Service Description  │
│  Commerce Core: Registry | Negotiation | Contract |      │
│                Verification | Reputation | Arbitration   │
│                Settlement | Team Formation                │
│  LLM Backend: Qwen3.7-Max | Qwen3-Coder | Qwen3.6-Plus  │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ |
| LLM | Qwen Cloud (Qwen3.7-Max, Qwen3-Coder, Qwen3.6-Plus) |
| Agent Framework | Custom lightweight (no LangChain) |
| Async | asyncio |
| Database | SQLite (MVP) → PostgreSQL (later) |
| API | FastAPI |
| Demo UI | Next.js + React Flow |
| Testing | pytest + pytest-asyncio |
| CI | GitHub Actions |
| License | MIT |

## Five-Week Schedule

### Week 1 (June 4–10): Foundation
- [x] Project scaffold, pyproject.toml, directory structure
- [x] 18 economic relationship types (protocol/types.py)
- [x] Shared data models (protocol/models.py)
- [x] Message bus (protocol/messaging.py)
- [x] Service Registry (registry/registry.py)
- [x] Qwen Cloud LLM wrapper (llm/qwen.py)
- [x] Base Agent class (agent.py)
- [x] Unit tests for all above
- [x] CI configuration (GitHub Actions)
- [x] Deliverable documents

### Week 2 (June 11–17): Negotiation + Contract
- [ ] Negotiation engine: multi-round with deadlock detection
- [ ] Negotiation strategies: tit-for-tat, concession, BATNA, value-based
- [ ] Contract Manager: create, sign, lifecycle tracking
- [ ] Integration: Negotiation → Contract (agreed deal → signed contract)
- [ ] Relationship types: Purchase + Commission + Contract
- [ ] Tests for negotiation and contract pipeline

### Week 3 (June 18–24): Trust Layer
- [ ] Delivery Verifier: automated acceptance checking
- [ ] Reputation System: ratings, time decay, transitive trust
- [ ] Credit ledger: balance tracking, transfer, audit
- [ ] Relationship types: Subscription + Open Bounty + Verification
- [ ] Tests for verification and reputation pipeline

### Week 4 (June 25 – July 1): Advanced + Demo
- [ ] Arbitration Agent: automated dispute resolution
- [ ] Team Formation: assemble, coordinate, disband, payout
- [ ] Demo scenario: Competitive Analysis Report orchestration
- [ ] Next.js UI: React Flow graph + floating cards + 7-scene demo
- [ ] Draft demo video recording

### Week 5 (July 2–8): Polish & Submit
- [ ] Architecture diagram (final)
- [ ] README.md + README_CN.md
- [ ] API documentation
- [ ] Demo video (final, <3 min, English voiceover)
- [ ] Alibaba Cloud deployment
- [ ] Devpost submission

## Key Design Decisions

1. **No LangChain**: Custom lightweight agent loop shows engineering depth
2. **Structured Protocol**: JSON messages between agents, not natural language
3. **Compose Over Inherit**: Capabilities injected, not baked into class hierarchy
4. **Test From Day 1**: Every module ships with tests
5. **Bilingual Docs**: Chinese for hackathon, English for global GitHub

## Post-Hackathon Roadmap

| Phase | Timeline | Goal |
|-------|----------|------|
| Hackathon | Week 1-5 | MVP, 8 CORE types, demo, submit |
| Launch | Week 6-8 | HN, V2EX, 掘金, r/LLMDevs. Target: 200+ stars |
| Community | Month 2-3 | Accept PRs, grow relationship types, improve docs |
| Protocol RFC | Month 3-6 | Publish ACP as standalone spec |
| Ecosystem | Month 6+ | SDK, marketplace, plugins |
