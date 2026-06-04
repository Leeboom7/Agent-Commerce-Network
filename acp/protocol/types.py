"""
Agent Commerce Protocol — Economic Relationship Types.

Defines all 18 types of economic relationships that AI agents can form.
Organized into 5 categories for conceptual clarity.

This is the canonical protocol specification. All implementations MUST
support at minimum the types marked as CORE.
"""

from enum import Enum


# ──────────────────────────────────────────────────────────────
# Category A: Discrete Transactions (一次性交易)
# ──────────────────────────────────────────────────────────────


class DiscreteTransactionType(str, Enum):
    """One-time, bounded transactions with clear deliverables."""

    PURCHASE = "purchase"
    """Buy a fixed service or product from another agent.

    Example: Agent A pays Agent B 50 credits for a market data report.
    Pricing: Fixed price or per-unit.
    Duration: One-shot delivery.
    CORE: Yes — fundamental economic primitive.
    """

    COMMISSION = "commission"
    """Delegate a sub-task to another agent.

    Example: An orchestrator agent commissions a translation agent to
    translate a document as part of a larger workflow.
    Pricing: Negotiated per-task.
    Duration: One-shot delivery with possible revision rounds.
    CORE: Yes — essential for task decomposition.
    """

    CONTRACT = "contract"
    """Formal project-based delivery with milestones and acceptance criteria.

    Example: A buyer agent contracts a developer agent to build a complete
    web scraper with 3 defined milestones, each with its own acceptance criteria.
    Pricing: Milestone-based with holdbacks.
    Duration: Multi-phase with defined deadline.
    CORE: Yes — the most formal discrete transaction type.
    """


# ──────────────────────────────────────────────────────────────
# Category B: Ongoing Relationships (持续关系)
# ──────────────────────────────────────────────────────────────


class OngoingRelationshipType(str, Enum):
    """Continuous, subscription-like relationships between agents."""

    SUBSCRIPTION = "subscription"
    """Subscribe to an agent's ongoing capability.

    Example: Orchestrator subscribes to a monitoring agent that continuously
    watches system metrics and alerts on anomalies. Billed monthly.
    Pricing: Recurring (per-period).
    Duration: Ongoing until cancelled.
    CORE: Yes — foundational for service-oriented agent economy.
    """

    RETAINER = "retainer"
    """Long-term advisor or embedded agent arrangement.

    Example: A startup agent retains a legal-review agent on a monthly
    retainer for 20 hours of contract review per month.
    Pricing: Periodic retainer fee with usage caps.
    Duration: Ongoing with periodic renewal.
    """

    FRANCHISE = "franchise"
    """License a workflow template or business model for replication.

    Example: Agent A developed a successful lead-generation workflow.
    Agent B pays a franchise fee + royalty to replicate it in a different market.
    Pricing: Upfront license fee + ongoing royalty percentage.
    Duration: Defined territory/period.
    """

    MODEL_RENTAL = "model_rental"
    """Rent access to a specialized model, dataset, or computational capability.

    Example: A small agent rents inference time on a fine-tuned Qwen model
    hosted by another agent that specializes in medical text analysis.
    Pricing: Per-token or per-inference.
    Duration: Pay-as-you-go or prepaid blocks.
    """


# ──────────────────────────────────────────────────────────────
# Category C: Intermediary & Platform (中介平台)
# ──────────────────────────────────────────────────────────────


class IntermediaryType(str, Enum):
    """Platform-like relationships where agents intermediate between others."""

    REFERRAL = "referral"
    """Refer a task or customer to another agent, earning a commission.

    Example: Agent A can't handle a complex data analysis request, so it
    refers the buyer to Agent B. Upon successful completion, Agent B pays
    Agent A a 10% referral fee.
    Pricing: Percentage of resulting transaction.
    Duration: Per-referral.
    """

    AGGREGATION = "aggregation"
    """Aggregate multiple agents' services into a unified offering.

    Example: Agent A offers a "Complete Market Intelligence" package that
    internally aggregates services from a data-scraper agent, an analyst
    agent, and a visualization agent — presenting one unified interface.
    Pricing: Markup on aggregated services.
    Duration: Per-transaction or subscription.
    """

    OPEN_BOUNTY = "open_bounty"
    """Post a task publicly; agents compete or bid to win the work.

    Example: An orchestrator posts a bounty: "Build a SQL query optimizer,
    budget 200 credits." Three developer agents submit proposals. The
    orchestrator picks one based on reputation, price, and proposed approach.
    Pricing: Fixed bounty or reverse auction.
    Duration: Defined submission window.
    CORE: Yes — critical for efficient task allocation in agent economy.
    """


# ──────────────────────────────────────────────────────────────
# Category D: Collaboration & Teams (协作团队)
# ──────────────────────────────────────────────────────────────


class CollaborationType(str, Enum):
    """Multi-agent coordination for complex outcomes."""

    TEAM_FORMATION = "team_formation"
    """Multiple agents form a temporary team for a complex outcome.

    Example: To generate a comprehensive industry report, an orchestrator
    assembles a team: data analyst + report writer + fact checker + designer.
    Team disbands after delivery. Members are paid per their contribution.
    Pricing: Pre-agreed split or proportional to contribution.
    Duration: Project duration.
    CORE: Yes — the ultimate Agent Society primitive.
    """

    JOINT_VENTURE = "joint_venture"
    """Agents co-invest resources and share risk/reward of an outcome.

    Example: Agent A (has distribution) and Agent B (has technology) form
    a joint venture to build and sell a new AI-powered tool. They split
    costs 50/50 and revenue 60/40 based on negotiated terms.
    Pricing: Cost-sharing + revenue-sharing agreement.
    Duration: Defined venture period.
    """

    REVENUE_SHARING = "revenue_sharing"
    """Split revenue generated from a shared outcome or product.

    Example: Three agents collaborate on an open-source library. Revenue
    from sponsorships and enterprise support is split per a predefined
    contribution-weighted formula.
    Pricing: Percentage-based split.
    Duration: Ongoing as long as revenue flows.
    """


# ──────────────────────────────────────────────────────────────
# Category E: Trust & Governance (信任治理)
# ──────────────────────────────────────────────────────────────


class TrustGovernanceType(str, Enum):
    """Trust, verification, and dispute resolution mechanisms."""

    VERIFICATION = "verification"
    """Verify or audit another agent's delivery against contract terms.

    Example: Before releasing payment, the buyer commissions a verifier
    agent to check that all acceptance criteria are met. The verifier
    produces a structured pass/fail report.
    Pricing: Per-verification fee.
    Duration: Per-audit.
    CORE: Yes — trust is impossible without verification.
    """

    ARBITRATION = "arbitration"
    """Resolve disputes between transacting agents.

    Example: Buyer claims delivery was substandard. Seller claims it met spec.
    Both agree to binding arbitration. The arbitrator reviews the contract,
    delivery, and evidence from both sides, then issues a ruling.
    Pricing: Arbitration fee (split or loser-pays).
    Duration: Per-case.
    CORE: Yes — disputes are inevitable in any economy.
    """

    INSURANCE = "insurance"
    """Provide delivery guarantee or underwrite transaction risk.

    Example: Agent A pays a 2% insurance premium. If the seller fails to
    deliver, the insurer pays out 80% of the contract value to Agent A.
    Pricing: Percentage-based premium.
    Duration: Per-transaction or blanket coverage.
    """

    ESCROW = "escrow"
    """Hold payment in escrow until delivery is verified.

    Example: Buyer deposits 100 credits into escrow. Seller delivers.
    Verifier approves. Escrow releases 95 to seller, 5 to verifier.
    If delivery fails, escrow returns 95 to buyer, 5 to verifier.
    Pricing: Flat or percentage fee.
    Duration: Per-transaction.
    """

    CAPITAL_ALLOCATION = "capital_allocation"
    """Invest credits/resources in an agent in exchange for future returns.

    Example: An investor agent identifies a high-potential new agent and
    allocates 1000 credits in exchange for 15% of that agent's future
    transaction revenue over the next 12 months.
    Pricing: Investment amount for equity-like stake.
    Duration: Defined investment period with exit terms.
    """


# ──────────────────────────────────────────────────────────────
# Unified Type Registry
# ──────────────────────────────────────────────────────────────


class EconomicRelationshipCategory(str, Enum):
    """Top-level categories of agent economic relationships."""
    DISCRETE_TRANSACTION = "discrete_transaction"
    ONGOING_RELATIONSHIP = "ongoing_relationship"
    INTERMEDIARY = "intermediary"
    COLLABORATION = "collaboration"
    TRUST_GOVERNANCE = "trust_governance"


# Maps each relationship type to its category
RELATIONSHIP_CATEGORY_MAP: dict[str, EconomicRelationshipCategory] = {
    # Discrete transactions
    "purchase": EconomicRelationshipCategory.DISCRETE_TRANSACTION,
    "commission": EconomicRelationshipCategory.DISCRETE_TRANSACTION,
    "contract": EconomicRelationshipCategory.DISCRETE_TRANSACTION,
    # Ongoing relationships
    "subscription": EconomicRelationshipCategory.ONGOING_RELATIONSHIP,
    "retainer": EconomicRelationshipCategory.ONGOING_RELATIONSHIP,
    "franchise": EconomicRelationshipCategory.ONGOING_RELATIONSHIP,
    "model_rental": EconomicRelationshipCategory.ONGOING_RELATIONSHIP,
    # Intermediary
    "referral": EconomicRelationshipCategory.INTERMEDIARY,
    "aggregation": EconomicRelationshipCategory.INTERMEDIARY,
    "open_bounty": EconomicRelationshipCategory.INTERMEDIARY,
    # Collaboration
    "team_formation": EconomicRelationshipCategory.COLLABORATION,
    "joint_venture": EconomicRelationshipCategory.COLLABORATION,
    "revenue_sharing": EconomicRelationshipCategory.COLLABORATION,
    # Trust & Governance
    "verification": EconomicRelationshipCategory.TRUST_GOVERNANCE,
    "arbitration": EconomicRelationshipCategory.TRUST_GOVERNANCE,
    "insurance": EconomicRelationshipCategory.TRUST_GOVERNANCE,
    "escrow": EconomicRelationshipCategory.TRUST_GOVERNANCE,
    "capital_allocation": EconomicRelationshipCategory.TRUST_GOVERNANCE,
}

# CORE types — recommended for MVP implementation
CORE_RELATIONSHIP_TYPES: set[str] = {
    "purchase",
    "commission",
    "contract",
    "subscription",
    "open_bounty",
    "team_formation",
    "verification",
    "arbitration",
}

# Total count for reference
TOTAL_RELATIONSHIP_TYPES = 18


def get_category(relationship_type: str) -> EconomicRelationshipCategory:
    """Get the category for a relationship type."""
    if relationship_type not in RELATIONSHIP_CATEGORY_MAP:
        raise ValueError(f"Unknown relationship type: {relationship_type}")
    return RELATIONSHIP_CATEGORY_MAP[relationship_type]


def is_core(relationship_type: str) -> bool:
    """Check if a relationship type is part of the CORE set."""
    return relationship_type in CORE_RELATIONSHIP_TYPES


def list_by_category(category: EconomicRelationshipCategory) -> list[str]:
    """List all relationship types in a given category."""
    return [
        rt for rt, cat in RELATIONSHIP_CATEGORY_MAP.items()
        if cat == category
    ]
