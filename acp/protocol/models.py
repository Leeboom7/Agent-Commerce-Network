"""
ACP Protocol — Shared Data Models.

All core dataclasses used across the Agent Commerce Protocol.
Models are designed to be serializable (JSON), introspectable,
and framework-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


# ──────────────────────────────────────────────────────────────
# Identity
# ──────────────────────────────────────────────────────────────


@dataclass
class AgentIdentity:
    """Unique identity for an agent in the commerce network."""

    agent_id: str
    name: str
    description: str = ""
    owner: str = ""  # Human or organization responsible
    public_key_pem: str = ""  # For future cryptographic signing
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, name: str, description: str = "", owner: str = "") -> AgentIdentity:
        return cls(
            agent_id=f"agent-{uuid4().hex[:12]}",
            name=name,
            description=description,
            owner=owner,
        )


# ──────────────────────────────────────────────────────────────
# Pricing
# ──────────────────────────────────────────────────────────────


class PricingModelType(str, Enum):
    FIXED = "fixed"  # One fixed price
    PER_TOKEN = "per_token"  # Per input/output token
    PER_UNIT = "per_unit"  # Per unit of work
    SUBSCRIPTION = "subscription"  # Recurring per period
    NEGOTIABLE = "negotiable"  # Price determined through negotiation
    AUCTION = "auction"  # Price determined by bidding


@dataclass
class PricingModel:
    """How an agent charges for its services."""

    model_type: PricingModelType
    base_price: float = 0.0
    currency: str = "NC"  # Network Credits (simulated currency in OSS version)
    price_per_token: float | None = None
    price_per_unit: float | None = None
    subscription_interval: str | None = None  # "daily", "weekly", "monthly"
    min_price: float | None = None  # For negotiable/auction types
    max_price: float | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def calculate(self, units: float = 1.0, tokens: int = 0) -> float:
        """Calculate the price for a given quantity."""
        if self.model_type == PricingModelType.FIXED:
            return self.base_price
        elif self.model_type == PricingModelType.PER_TOKEN:
            return (self.price_per_token or 0.0) * tokens
        elif self.model_type == PricingModelType.PER_UNIT:
            return (self.price_per_unit or 0.0) * units
        elif self.model_type == PricingModelType.SUBSCRIPTION:
            return self.base_price
        else:
            return self.base_price  # negotiable/auction — base is starting point


# ──────────────────────────────────────────────────────────────
# Availability
# ──────────────────────────────────────────────────────────────


@dataclass
class AvailabilitySpec:
    """When and how an agent is available."""

    mode: str = "on_demand"  # "always_on", "scheduled", "on_demand"
    max_concurrent_tasks: int = 5
    typical_latency_ms: int = 5000
    uptime_sla: float = 0.99
    active_hours: str | None = None  # cron expression or time range
    cooldown_ms: int = 1000  # Minimum delay between requests


# ──────────────────────────────────────────────────────────────
# Service Listing
# ──────────────────────────────────────────────────────────────


@dataclass
class ServiceListing:
    """A service offered by an agent on the commerce network."""

    listing_id: str = field(default_factory=lambda: f"listing-{uuid4().hex[:12]}")
    agent_id: str = ""
    service_type: str = ""  # e.g., "data_analysis", "report_writing", "code_review"
    economic_relationship: str = ""  # One of the 18 relationship types
    title: str = ""
    description: str = ""
    capabilities: dict[str, Any] = field(default_factory=dict)
    pricing: PricingModel = field(default_factory=lambda: PricingModel(model_type=PricingModelType.NEGOTIABLE))
    availability: AvailabilitySpec = field(default_factory=AvailabilitySpec)
    tags: list[str] = field(default_factory=list)
    reputation_score: float = 100.0  # Initial score for new agents (neutral)
    total_transactions: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def matches_query(self, query: str) -> bool:
        """Simple keyword matching for discovery."""
        query_lower = query.lower()
        searchable = f"{self.title} {self.description} {self.service_type} {' '.join(self.tags)}"
        return query_lower in searchable.lower()

    def matches_capability(self, required: dict[str, Any]) -> bool:
        """Check if this service satisfies required capabilities."""
        for key, value in required.items():
            if key not in self.capabilities:
                return False
            if self.capabilities[key] != value:
                return False
        return True


# ──────────────────────────────────────────────────────────────
# Contract Terms
# ──────────────────────────────────────────────────────────────


@dataclass
class ContractTerms:
    """The specific terms of a service agreement."""

    price: float
    currency: str = "NC"
    deadline: str = ""  # ISO 8601 datetime
    deliverables: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    revision_rounds: int = 2  # Max revision rounds included in price
    penalty_rate: float = 0.10  # Penalty as fraction of price for non-delivery
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "price": self.price,
            "currency": self.currency,
            "deadline": self.deadline,
            "deliverables": self.deliverables,
            "acceptance_criteria": self.acceptance_criteria,
            "revision_rounds": self.revision_rounds,
            "penalty_rate": self.penalty_rate,
            "metadata": self.metadata,
        }


# ──────────────────────────────────────────────────────────────
# Messages
# ──────────────────────────────────────────────────────────────


class MessageType(str, Enum):
    """Types of messages in the agent communication protocol."""

    # Discovery
    REGISTER_SERVICE = "register_service"
    SEARCH_REQUEST = "search_request"
    SEARCH_RESPONSE = "search_response"

    # Negotiation
    NEGOTIATION_OFFER = "negotiation_offer"
    NEGOTIATION_COUNTER = "negotiation_counter"
    NEGOTIATION_ACCEPT = "negotiation_accept"
    NEGOTIATION_REJECT = "negotiation_reject"
    NEGOTIATION_WITHDRAW = "negotiation_withdraw"

    # Contract
    CONTRACT_PROPOSE = "contract_propose"
    CONTRACT_SIGN = "contract_sign"
    CONTRACT_DELIVER = "contract_deliver"
    CONTRACT_ACCEPT = "contract_accept"
    CONTRACT_REJECT = "contract_reject"
    CONTRACT_DISPUTE = "contract_dispute"

    # Verification
    VERIFICATION_REQUEST = "verification_request"
    VERIFICATION_REPORT = "verification_report"

    # Arbitration
    ARBITRATION_FILE = "arbitration_file"
    ARBITRATION_EVIDENCE = "arbitration_evidence"
    ARBITRATION_RULING = "arbitration_ruling"

    # Settlement
    PAYMENT_TRANSFER = "payment_transfer"
    PAYMENT_CONFIRMATION = "payment_confirmation"

    # Reputation
    RATING_SUBMIT = "rating_submit"

    # Team
    TEAM_INVITE = "team_invite"
    TEAM_JOIN = "team_join"
    TEAM_TASK_ASSIGN = "team_task_assign"
    TEAM_DISBAND = "team_disband"

    # System
    ERROR = "error"
    ACKNOWLEDGMENT = "acknowledgment"


@dataclass
class AgentMessage:
    """A structured message between agents in the commerce network."""

    message_id: str = field(default_factory=lambda: f"msg-{uuid4().hex[:12]}")
    sender_id: str = ""
    receiver_id: str = ""
    message_type: MessageType = MessageType.ACKNOWLEDGMENT
    payload: dict[str, Any] = field(default_factory=dict)
    references: list[str] = field(default_factory=list)  # References to prior messages
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "message_type": self.message_type.value,
            "payload": self.payload,
            "references": self.references,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentMessage:
        return cls(
            message_id=data.get("message_id", ""),
            sender_id=data["sender_id"],
            receiver_id=data["receiver_id"],
            message_type=MessageType(data["message_type"]),
            payload=data.get("payload", {}),
            references=data.get("references", []),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data
            else datetime.now(timezone.utc),
        )


# ──────────────────────────────────────────────────────────────
# Negotiation
# ──────────────────────────────────────────────────────────────


@dataclass
class NegotiationRound:
    """A single round in a negotiation session."""

    round_number: int
    offer: ContractTerms
    counter_offer: ContractTerms | None = None
    rationale: str = ""  # Agent's reasoning for this offer
    strategy_used: str = ""  # e.g., "tit-for-tat", "concession", "BATNA"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "round_number": self.round_number,
            "offer": self.offer.to_dict(),
            "counter_offer": self.counter_offer.to_dict() if self.counter_offer else None,
            "rationale": self.rationale,
            "strategy_used": self.strategy_used,
            "timestamp": self.timestamp.isoformat(),
        }


class NegotiationStatus(str, Enum):
    ACTIVE = "active"
    AGREED = "agreed"
    DEADLOCKED = "deadlocked"
    WITHDRAWN = "withdrawn"


@dataclass
class NegotiationSession:
    """A complete negotiation between a buyer and seller agent."""

    session_id: str = field(default_factory=lambda: f"neg-{uuid4().hex[:12]}")
    buyer_id: str = ""
    seller_id: str = ""
    relationship_type: str = "purchase"
    rounds: list[NegotiationRound] = field(default_factory=list)
    status: NegotiationStatus = NegotiationStatus.ACTIVE
    max_rounds: int = 10
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: datetime | None = None

    @property
    def current_round(self) -> int:
        return len(self.rounds)

    @property
    def latest_offer(self) -> ContractTerms | None:
        if not self.rounds:
            return None
        last = self.rounds[-1]
        return last.counter_offer or last.offer

    def is_exhausted(self) -> bool:
        return self.current_round >= self.max_rounds


# ──────────────────────────────────────────────────────────────
# Contract
# ──────────────────────────────────────────────────────────────


class ContractStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DELIVERED = "delivered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DISPUTED = "disputed"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"


@dataclass
class ServiceContract:
    """A binding agreement between transacting agents."""

    contract_id: str = field(default_factory=lambda: f"contract-{uuid4().hex[:12]}")
    parties: list[str] = field(default_factory=list)  # [buyer_id, seller_id]
    relationship_type: str = "purchase"
    terms: ContractTerms = field(default_factory=lambda: ContractTerms(price=0.0))
    status: ContractStatus = ContractStatus.DRAFT
    negotiation_session_id: str | None = None
    delivery_attempts: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fulfilled_at: datetime | None = None

    @property
    def buyer_id(self) -> str:
        return self.parties[0] if self.parties else ""

    @property
    def seller_id(self) -> str:
        return self.parties[1] if len(self.parties) > 1 else ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "parties": self.parties,
            "relationship_type": self.relationship_type,
            "terms": self.terms.to_dict(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }


# ──────────────────────────────────────────────────────────────
# Reputation
# ──────────────────────────────────────────────────────────────


@dataclass
class Rating:
    """A rating submitted after a transaction."""

    rating_id: str = field(default_factory=lambda: f"rating-{uuid4().hex[:12]}")
    rater_id: str = ""
    transaction_id: str = ""
    scores: dict[str, float] = field(default_factory=dict)
    # Typical score dimensions: quality, timeliness, communication, accuracy
    comment: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def overall(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)


@dataclass
class ReputationRecord:
    """Accumulated reputation data for an agent."""

    agent_id: str
    ratings: list[Rating] = field(default_factory=list)
    composite_score: float = 100.0  # 0-100, starts neutral
    trust_graph: dict[str, float] = field(default_factory=dict)  # agent_id -> trust score
    total_volume: int = 0  # Total credits transacted
    total_transactions: int = 0
    successful_transactions: int = 0
    disputed_transactions: int = 0

    @property
    def success_rate(self) -> float:
        if self.total_transactions == 0:
            return 1.0
        return self.successful_transactions / self.total_transactions


# ──────────────────────────────────────────────────────────────
# Settlement
# ──────────────────────────────────────────────────────────────


@dataclass
class TransactionRecord:
    """A record of credit transfer between agents."""

    transaction_id: str = field(default_factory=lambda: f"txn-{uuid4().hex[:12]}")
    from_agent_id: str = ""
    to_agent_id: str = ""
    amount: float = 0.0
    currency: str = "NC"
    contract_id: str = ""
    reason: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ──────────────────────────────────────────────────────────────
# Team
# ──────────────────────────────────────────────────────────────


class TeamRole(str, Enum):
    LEAD = "lead"
    MEMBER = "member"
    OBSERVER = "observer"


@dataclass
class TeamMember:
    agent_id: str
    role: TeamRole = TeamRole.MEMBER
    assigned_tasks: list[str] = field(default_factory=list)
    payout_share: float = 0.0  # Fraction of total payment


@dataclass
class Team:
    """A temporary team of agents collaborating on a complex task."""

    team_id: str = field(default_factory=lambda: f"team-{uuid4().hex[:12]}")
    name: str = ""
    members: list[TeamMember] = field(default_factory=list)
    contract_id: str = ""  # The contract this team is fulfilling
    status: str = "forming"  # forming / active / delivering / disbanded
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ──────────────────────────────────────────────────────────────
# Verification
# ──────────────────────────────────────────────────────────────


@dataclass
class CheckResult:
    """Result of an individual acceptance criterion check."""

    criterion: str
    passed: bool
    actual_value: Any = None
    expected_value: Any = None
    notes: str = ""


@dataclass
class VerificationReport:
    """A report produced by a verifier agent assessing a delivery."""

    report_id: str = field(default_factory=lambda: f"verif-{uuid4().hex[:12]}")
    contract_id: str = ""
    verifier_id: str = ""
    checks: list[CheckResult] = field(default_factory=list)
    verdict: str = ""  # "accepted", "rejected", "partial"
    summary: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def passed_count(self) -> int:
        return sum(1 for c in self.checks if c.passed)

    @property
    def total_count(self) -> int:
        return len(self.checks)

    @property
    def pass_rate(self) -> float:
        if not self.checks:
            return 0.0
        return self.passed_count / self.total_count


# ──────────────────────────────────────────────────────────────
# Market Context (for negotiation)
# ──────────────────────────────────────────────────────────────


@dataclass
class MarketContext:
    """Market data available to negotiation strategies."""

    recent_transaction_prices: list[float] = field(default_factory=list)
    average_price: float = 0.0
    price_range: tuple[float, float] = (0.0, 0.0)
    counterparty_reputation: float = 100.0
    counterparty_volume: int = 0
    demand_level: float = 0.5  # 0-1, higher means more demand
    supply_level: float = 0.5  # 0-1, higher means more supply

    @property
    def market_power(self) -> float:
        """Positive = seller's market, negative = buyer's market."""
        return self.demand_level - self.supply_level
