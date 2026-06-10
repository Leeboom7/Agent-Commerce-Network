# ACP Open-Source vs Private — Scope Boundary

This document defines the exact boundary between the open-source (hackathon) edition and the private production edition of the Agent Commerce Network.

---

## Guiding Principle

The open-source edition demonstrates the **architecture, protocol design, and economic model** of the Agent Commerce Network. It is a fully functional, self-contained system that anyone can run. The private edition adds **blockchain settlement, advanced security, production infrastructure, and commercial features**.

---

## Open-Source Edition (Hackathon)

### Included

| Component | Status | Description |
|-----------|--------|-------------|
| **Protocol Definition** | ✅ Complete | All 18 economic relationship types defined in `acp/protocol/types.py` |
| **Data Models** | ✅ Complete | All shared dataclasses: AgentIdentity, ServiceListing, ContractTerms, AgentMessage, etc. |
| **Message Bus** | ✅ Complete | In-memory async message bus for agent-agent communication |
| **Service Registry** | ✅ Complete | Registration, discovery, search with multi-criteria filtering |
| **Negotiation Engine** | ✅ Complete | Multi-round negotiation with 4 strategies (tit-for-tat, concession, BATNA, value-based) |
| **Contract Manager** | ✅ Complete | Contract lifecycle: draft → active → delivered → accepted/disputed → resolved |
| **Delivery Verifier** | ✅ Complete | Automated acceptance checking against contract criteria |
| **Reputation System** | ✅ Complete | Direct ratings, time-weighted composite, transitive trust |
| **Arbitration Agent** | ✅ Complete | Automated dispute resolution with reasoned rulings |
| **Settlement Ledger** | ✅ Complete | Credit system (Network Credits) with transaction history |
| **Team Formation** | ✅ Complete | Temporary team assembly, coordination, disbanding, payout |
| **Qwen LLM Wrapper** | ✅ Complete | Thin client for Qwen Cloud (Qwen3.7-Max, Qwen3-Coder, Qwen3.6-Plus) |
| **Base Agent Class** | ✅ Complete | Composable agent base with registry, messaging, LLM access |
| **Demo Scenario** | ✅ Complete | Competitive analysis report generation with 5 agents |
| **Demo UI** | ✅ Complete | Next.js Agent Commerce Theater with deterministic CSS/SVG staging, transaction objects, conflict scenes, and baseline proof |
| **Tests** | ✅ Complete | Unit tests for all core modules |
| **CI** | ✅ Complete | GitHub Actions: lint, type-check, test |
| **Documentation** | ✅ Complete | README (EN+CN), protocol spec, architecture diagram, demo video |
| **License** | ✅ MIT | Permissive open-source license |

### Excluded

| Component | Reason |
|-----------|--------|
| Blockchain smart contracts | Kept private — core IP for production edition |
| Stablecoin payment integration | Kept private — requires regulatory compliance infrastructure |
| Production deployment (K8s, monitoring, autoscaling) | Not applicable to open-source demo |
| Anti-Sybil / advanced fraud detection | Kept private — proprietary security algorithms |
| Revenue sharing and commercial licensing logic | Kept private — business model IP |
| Enterprise SSO / RBAC | Not applicable to open-source edition |
| SLA enforcement automation | Kept private — production orchestration logic |
| Multi-region deployment configs | Not applicable to open-source edition |

---

## Private Edition

### Core IP (Not in Open-Source)

| Component | Description |
|-----------|-------------|
| **Blockchain Settlement Layer** | Smart contracts for autonomous agent-to-agent payments on-chain. Supports multiple chains and stablecoins (USDC, USDT). |
| **Token Economics** | Native token design, staking mechanisms, slashing conditions, liquidity pools. |
| **On-Chain Reputation** | Soul-bound NFTs for agent identity and reputation, cross-chain reputation portability. |
| **Production Infrastructure** | Kubernetes orchestration, auto-scaling, multi-region deployment, DDoS protection, rate limiting. |
| **Advanced Fraud Detection** | ML-based Sybil detection, collusion ring identification, wash-trading detection. |
| **Fiat On/Off-Ramp** | Integration with licensed payment service providers for fiat-to-crypto conversion. |
| **Enterprise Features** | SSO, RBAC, audit logging, compliance reporting, SLA guarantees. |
| **Marketplace** | Curated agent directory with featured listings, sponsored placement, quality badges. |

---

## Why This Boundary?

1. **Intellectual Property Protection**: The blockchain settlement layer and token economics are the core commercial IP. Releasing them as open-source would eliminate the commercial moat.

2. **Regulatory Compliance**: Stablecoin payment processing requires licenses and compliance infrastructure that cannot be open-sourced.

3. **Community Building**: The open-source edition is the "developer preview" — it lets anyone experiment with ACP, build agents, and contribute to the protocol. Developers who build on the open-source edition are natural customers for the production edition.

4. **Security**: Production security measures (anti-Sybil, fraud detection) lose effectiveness if their algorithms are public.

5. **Hackathon Requirements**: The Qwen Cloud Hackathon requires open-source code with a license. The open-source edition satisfies this requirement while protecting core IP.

---

## Transition Path

```
Open-Source Edition (Hackathon)
    │
    │  Community adoption, GitHub stars, developer feedback
    │
    ▼
Open-Source Protocol Standard (Post-Hackathon)
    │
    │  RFC published, third-party implementations, ecosystem growth
    │
    ▼
Production Edition (Private Beta)
    │
    │  Invite-only access, real payments, enterprise customers
    │
    ▼
Platform Launch
    │
    │  Public marketplace, developer SDK, revenue
    │
    ▼
Ecosystem
```

The open-source edition is the **top of the funnel**. The private edition is the **monetization layer**.
