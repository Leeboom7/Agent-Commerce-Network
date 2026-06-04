# Agent Commerce Network (ACP)

[![CI](https://github.com/your-username/agent-commerce-network/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/agent-commerce-network/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

**Economic infrastructure for the AI agent economy.**

The Agent Commerce Protocol (ACP) enables AI agents to autonomously:
- 🔍 **Discover** each other's services in a shared registry
- 🤝 **Negotiate** prices and terms using structured strategies
- 📝 **Sign** enforceable contracts with machine-verifiable criteria
- ✅ **Verify** deliveries automatically against acceptance criteria
- ⭐ **Build** reputation through time-weighted ratings and transitive trust
- ⚖️ **Resolve** disputes via automated arbitration
- 👥 **Form** temporary teams for complex multi-agent outcomes
- 💰 **Settle** payments through a transparent credit ledger

> **This is the community (open-source) edition.** A production version with blockchain settlement, advanced security, and enterprise features is under development. See [docs/scope-boundary.md](docs/scope-boundary.md) for details.

## Why ACP?

Current AI agent frameworks (LangChain, CrewAI, AutoGen) focus on **how agents execute tasks**. ACP focuses on **how agents transact with each other** — the economic layer that makes autonomous agent economies possible.

| Without ACP | With ACP |
|-------------|----------|
| Agents are hard-coded to call specific APIs | Agents discover services dynamically in a marketplace |
| No price discovery — dev sets prices manually | Agents negotiate prices based on market conditions |
| Trust is implicit ("I trust this API because I coded it") | Trust is earned through verifiable reputation |
| No recourse when an agent fails | Structured arbitration with penalty mechanisms |

## Quick Start

```bash
# Clone
git clone https://github.com/your-username/agent-commerce-network.git
cd agent-commerce-network

# Install
pip install -e ".[demo]"

# Set your Qwen API key
export QWEN_API_KEY=your-key-here

# Run the demo
python -m streamlit run demo/app.py
```

## Architecture

```
Agent Layer  →  Buyer, Seller, Arbitrator, Verifier agents
    ↕
ACP SDK      →  Identity, Messaging, Service Descriptions
    ↕
Commerce     →  Registry | Negotiation | Contract | Verification
Core            Reputation | Arbitration | Settlement | Teams
    ↕
LLM Backend  →  Qwen3.7-Max | Qwen3-Coder | Qwen3.6-Plus
```

## Economic Relationship Types

ACP defines **18 economic relationship types** across 5 categories:

| Category | Types | CORE (MVP) |
|----------|-------|------------|
| Discrete Transactions | Purchase, Commission, Contract | 3/3 |
| Ongoing Relationships | Subscription, Retainer, Franchise, Model Rental | 1/4 |
| Intermediary & Platform | Referral, Aggregation, Open Bounty | 1/3 |
| Collaboration & Teams | Team Formation, Joint Venture, Revenue Sharing | 1/3 |
| Trust & Governance | Verification, Arbitration, Insurance, Escrow, Capital Allocation | 2/5 |

See [docs/protocol-spec.md](docs/protocol-spec.md) for the full specification.

## Project Structure

```
agent-commerce-network/
├── acp/                    # Core protocol library
│   ├── protocol/           # Types, models, messaging
│   ├── registry/           # Service discovery
│   ├── negotiation/        # Multi-round negotiation engine
│   ├── contract/           # Contract lifecycle management
│   ├── verification/       # Automated delivery checking
│   ├── reputation/         # Ratings, trust, decay
│   ├── arbitration/        # Dispute resolution
│   ├── settlement/         # Credit ledger
│   ├── team/               # Team formation & coordination
│   ├── relationships/      # Economic relationship implementations
│   └── llm/                # Qwen Cloud integration
├── demo/                   # Streamlit demo application
├── tests/                  # pytest test suite
├── docs/                   # Documentation
└── deploy/                 # Deployment guides
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check acp/

# Type check
mypy acp/ --ignore-missing-imports
```

## Hackathon

This project is an entry in the **Qwen Cloud Global AI Hackathon (Track 3: Agent Society)**.

- **Deadline**: July 9, 2026
- **Platform**: [Devpost](https://qwencloud-hackathon.devpost.com/)
- **Tech Stack**: Qwen3.7-Max, Qwen3-Coder, Alibaba Cloud, Python, Streamlit

## License

MIT — see [LICENSE](LICENSE) file.

---

*Built with Qwen Cloud. The Agent Commerce Protocol is a community-driven specification.*
