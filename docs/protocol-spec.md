# Agent Commerce Protocol (ACP) — Protocol Specification v0.1.0

## Abstract

The Agent Commerce Protocol (ACP) defines a standardized economic infrastructure layer for AI agents. It enables agents to autonomously discover each other, negotiate prices and terms, sign enforceable contracts, verify deliveries, build and query reputation, resolve disputes, form temporary teams, and settle payments.

ACP is to the AI agent economy what TCP/IP is to the internet: a shared protocol that enables interoperability between independently developed agents, regardless of their internal implementation.

---

## 1. Economic Relationship Model

ACP defines **18 economic relationship types** organized into 5 categories. Every interaction between agents in the commerce network maps to one of these types.

### Category A: Discrete Transactions (一次性交易)

One-time, bounded transactions with clear deliverables.

| # | Type | Description | CORE |
|---|------|-------------|------|
| 1 | **Purchase** | Buy a fixed service or product from another agent. Pricing: fixed or per-unit. Duration: one-shot. | ✅ |
| 2 | **Commission** | Delegate a sub-task to another agent as part of a larger workflow. Pricing: negotiated per-task. | ✅ |
| 3 | **Contract** | Formal project-based delivery with milestones and acceptance criteria. Pricing: milestone-based. | ✅ |

### Category B: Ongoing Relationships (持续关系)

Continuous, subscription-like relationships between agents.

| # | Type | Description | CORE |
|---|------|-------------|------|
| 4 | **Subscription** | Subscribe to an agent's ongoing capability. Pricing: recurring per-period. | ✅ |
| 5 | **Retainer** | Long-term advisor or embedded agent arrangement with usage caps. | |
| 6 | **Franchise** | License a workflow template or business model for replication. | |
| 7 | **Model Rental** | Rent access to a specialized model, dataset, or computational capability. | |

### Category C: Intermediary & Platform (中介平台)

Platform-like relationships where agents intermediate between others.

| # | Type | Description | CORE |
|---|------|-------------|------|
| 8 | **Referral** | Refer a task/customer to another agent, earn commission on completion. | |
| 9 | **Aggregation** | Aggregate multiple agents' services into a unified offering with markup. | |
| 10 | **Open Bounty** | Post a task publicly; agents compete or bid to win the work. | ✅ |

### Category D: Collaboration & Teams (协作团队)

Multi-agent coordination for complex outcomes.

| # | Type | Description | CORE |
|---|------|-------------|------|
| 11 | **Team Formation** | Multiple agents form a temporary team for a complex outcome, disbanding after delivery. | ✅ |
| 12 | **Joint Venture** | Agents co-invest resources and share risk/reward of a defined venture. | |
| 13 | **Revenue Sharing** | Split revenue from a shared outcome per a contribution-weighted formula. | |

### Category E: Trust & Governance (信任治理)

Trust, verification, and dispute resolution mechanisms.

| # | Type | Description | CORE |
|---|------|-------------|------|
| 14 | **Verification** | Verify/audit another agent's delivery against contract terms. | ✅ |
| 15 | **Arbitration** | Resolve disputes between transacting agents with binding rulings. | ✅ |
| 16 | **Insurance** | Provide delivery guarantee or underwrite transaction risk. | |
| 17 | **Escrow** | Hold payment in escrow until delivery is verified, then release. | |
| 18 | **Capital Allocation** | Invest credits in an agent in exchange for future revenue share. | |

**Legend**: ✅ = CORE type (8 total), implemented in MVP. Others defined in protocol, implementation planned.

---

## 2. Protocol Layers

```
┌─────────────────────────────────────────┐
│  Application Layer                       │
│  (Demo agents, custom implementations)   │
├─────────────────────────────────────────┤
│  Commerce Layer                          │
│  Registry | Negotiation | Contract |     │
│  Verification | Reputation | Arbitration│
│  Settlement | Team Formation             │
├─────────────────────────────────────────┤
│  Message Layer                           │
│  AgentMessage | MessageBus | Routing     │
├─────────────────────────────────────────┤
│  Identity Layer                          │
│  AgentIdentity | ServiceListing          │
├─────────────────────────────────────────┤
│  Transport Layer                         │
│  In-Memory (MVP) | Redis | gRPC (future) │
└─────────────────────────────────────────┘
```

---

## 3. Message Protocol

### Message Format

All agent-to-agent communication uses structured JSON messages:

```json
{
  "message_id": "msg-a1b2c3d4e5f6",
  "sender_id": "agent-data-analyst-001",
  "receiver_id": "agent-orchestrator-001",
  "message_type": "negotiation_offer",
  "payload": {
    "price": 50.0,
    "currency": "NC",
    "deadline": "2026-07-01T00:00:00Z",
    "deliverables": ["market_data.csv", "analysis_report.md"]
  },
  "references": ["msg-previous-001"],
  "timestamp": "2026-06-10T12:00:00Z"
}
```

### Message Types

| Category | Types |
|----------|-------|
| **Discovery** | register_service, search_request, search_response |
| **Negotiation** | negotiation_offer, negotiation_counter, negotiation_accept, negotiation_reject, negotiation_withdraw |
| **Contract** | contract_propose, contract_sign, contract_deliver, contract_accept, contract_reject, contract_dispute |
| **Verification** | verification_request, verification_report |
| **Arbitration** | arbitration_file, arbitration_evidence, arbitration_ruling |
| **Settlement** | payment_transfer, payment_confirmation |
| **Reputation** | rating_submit |
| **Team** | team_invite, team_join, team_task_assign, team_disband |
| **System** | error, acknowledgment |

---

## 4. Negotiation Protocol

### State Machine

```
    ┌─────────┐
    │  START  │
    └────┬────┘
         ↓
    ┌─────────┐     reject     ┌────────────┐
    │  ACTIVE  │──────────────→│ DEADLOCKED  │
    └────┬────┘                └────────────┘
         │ agree                    ↑
         ↓                    max rounds
    ┌─────────┐               exhausted
    │ AGREED  │                    ↑
    └────┬────┘               withdraw
         ↓                    ┌────────────┐
    ┌─────────┐               │ WITHDRAWN  │
    │CONTRACT │               └────────────┘
    └─────────┘
```

### Round Structure

Each negotiation round:
1. **Offer**: Proposing agent submits `ContractTerms` with rationale
2. **Counter-offer** (optional): Receiving agent submits revised `ContractTerms`
3. **Decision**: Accept → moves to AGREED; Reject → next round or DEADLOCKED

### Strategies

| Strategy | Description |
|----------|-------------|
| **Tit-for-Tat** | Mirror the counterparty's concession pattern |
| **Concession-Based** | Gradually concede from opening to reservation price |
| **BATNA-Driven** | Calculate Best Alternative To Negotiated Agreement; walk if offer below BATNA value |
| **Value-Based** | Argue based on market comparables and value delivered |

---

## 5. Reputation Model

### Components

1. **Direct Ratings**: Per-transaction scores (quality, timeliness, communication, accuracy)
2. **Time-Weighted Composite**: Recent ratings matter more than old ones (90-day half-life)
3. **Transitive Trust**: A trusts B, B trusts C → A can estimate trust for C
4. **Stake-Backed Reputation** (production only): Agents stake tokens; poor behavior risks slashing

### Formula

```
composite_score = Σ(rating × e^(-λ × age)) / Σ(e^(-λ × age))

where λ = ln(2) / half_life_days
```

---

## 6. Settlement

### MVP (Open-Source Edition)

- **Currency**: Network Credits (NC) — simulated currency
- **Ledger**: In-memory transaction log (designed for SQLite/PostgreSQL migration)
- **Initial Balance**: Each new agent receives 1000 NC
- **Fees**: None in MVP; protocol supports configurable fee rates

### Production Edition (Private)

- Supports integration with: fiat payment gateways, stablecoin settlement (USDC/USDT), digital RMB (e-CNY)
- Blockchain-based smart contracts for autonomous settlement
- On-chain reputation NFTs

---

## 7. Implementation Caveats (MVP)

### Verification

The current delivery verifier is an **L0 heuristic engine**: it checks
format markers, presence of keywords, numeric thresholds, and citation
indicators using rule-based patterns. Vague or qualitative acceptance
criteria default to `passed=true` with a note. This is intentional for
the MVP — in production, verification should be augmented with LLM-based
semantic evaluation for qualitative criteria.

### Arbitration

The arbitration engine uses a **deterministic rule tree** based on
verification verdicts and contract status. It does not perform
independent evidence analysis or legal reasoning. This is sufficient for
protocol demonstration but is not a substitute for human or LLM-augmented
arbitration in high-stakes disputes.

### Signatures

Contract signatures are tracked via a dynamic `_signatures` list on the
contract object (MVP simplification). A production implementation should
use cryptographic signatures and store them as immutable contract metadata.

---

## 8. Compliance & Extensions

### What This Protocol Does NOT Specify

- Identity verification of the human/organization behind an agent
- Legal enforceability of agent-signed contracts in any jurisdiction
- KYC/AML for agent-to-agent payments
- Specific LLM model requirements (agents may use any model)

### Extension Points

- **Custom Relationship Types**: Implementations may define additional types beyond the 18
- **Custom Pricing Models**: Plug in any pricing function
- **Custom Negotiation Strategies**: Implement the strategy interface
- **Transport Backends**: Replace in-memory bus with Redis, gRPC, or message queues

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-06-04 | Initial protocol spec. All 18 types defined. 8 CORE types implemented in MVP. |
