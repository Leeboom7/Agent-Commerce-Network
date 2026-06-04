# Contributing to Agent Commerce Network

Thanks for your interest in contributing! ACP is a community-driven protocol for AI agent commerce.

## Ways to Contribute

### 1. Implement a New Economic Relationship Type

The protocol defines 18 types but the MVP implements 8 CORE types. Pick one of the unimplemented types and add it to `acp/relationships/`:

- **Retainer** — Long-term advisor arrangement
- **Franchise** — License a workflow template
- **Model Rental** — Rent model access
- **Referral** — Commission-based referral
- **Aggregation** — Aggregate multiple services
- **Joint Venture** — Co-investment with risk/reward sharing
- **Revenue Sharing** — Split revenue from shared outcomes
- **Insurance** — Delivery guarantee / risk underwriting
- **Escrow** — Third-party payment holding
- **Capital Allocation** — Invest in agents for future returns

### 2. Add a Negotiation Strategy

Current strategies: Tit-for-Tat, Concession, BATNA, Value-Based.
Add a new strategy to `acp/negotiation/strategies.py`:
- Anchoring-based
- Auction-style
- Relationship-based (long-term discount)
- Multi-issue (trade-off across multiple dimensions)

### 3. Improve the Delivery Verifier

The current verifier uses heuristic rules. Contributions welcome:
- LLM-augmented verification mode
- More format checkers (PDF, PPTX)
- Structured data comparison (diff two JSON objects against schema)

### 4. Add Transport Backends

The message bus currently supports in-memory only. Add:
- Redis Pub/Sub backend
- gRPC backend
- WebSocket backend

## Development Setup

```bash
git clone https://github.com/your-username/agent-commerce-network.git
cd agent-commerce-network
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check acp/

# Type check
mypy acp/ --ignore-missing-imports
```

## Pull Request Process

1. Fork the repo and create a feature branch
2. Add tests for your changes
3. Ensure all tests pass: `pytest tests/ -v`
4. Run lint: `ruff check acp/`
5. Update documentation if needed
6. Submit a PR with a clear description

## Code Style

- Python 3.12+ with type hints
- Follow existing patterns (dataclasses, composition over inheritance)
- Tests are required for new features
- Docstrings for public APIs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
