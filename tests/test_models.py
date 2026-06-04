"""Tests for shared protocol data models."""

from acp.protocol.models import (
    AgentIdentity,
    AgentMessage,
    ContractTerms,
    MessageType,
    NegotiationRound,
    NegotiationSession,
    NegotiationStatus,
    PricingModel,
    PricingModelType,
    Rating,
    ServiceListing,
)


class TestAgentIdentity:
    def test_create_identity(self) -> None:
        identity = AgentIdentity.create("TestAgent", "A test agent", "owner@example.com")
        assert identity.name == "TestAgent"
        assert identity.description == "A test agent"
        assert identity.agent_id.startswith("agent-")
        assert len(identity.agent_id) == 18  # "agent-" + 12 hex chars

    def test_unique_ids(self) -> None:
        a = AgentIdentity.create("A")
        b = AgentIdentity.create("B")
        assert a.agent_id != b.agent_id


class TestPricingModel:
    def test_fixed_price(self) -> None:
        model = PricingModel(model_type=PricingModelType.FIXED, base_price=100.0)
        assert model.calculate() == 100.0
        assert model.calculate(units=5) == 100.0  # Fixed ignores quantity

    def test_per_token_price(self) -> None:
        model = PricingModel(
            model_type=PricingModelType.PER_TOKEN,
            price_per_token=0.001,
        )
        assert model.calculate(tokens=5000) == 5.0

    def test_per_unit_price(self) -> None:
        model = PricingModel(
            model_type=PricingModelType.PER_UNIT,
            price_per_unit=10.0,
        )
        assert model.calculate(units=3) == 30.0

    def test_subscription_price(self) -> None:
        model = PricingModel(
            model_type=PricingModelType.SUBSCRIPTION,
            base_price=200.0,
            subscription_interval="monthly",
        )
        assert model.calculate() == 200.0


class TestServiceListing:
    def test_create_listing(self) -> None:
        listing = ServiceListing(
            agent_id="agent-001",
            service_type="data_analysis",
            economic_relationship="purchase",
            title="Market Data Analysis",
            description="Analyze market data and produce insights",
        )
        assert listing.listing_id.startswith("listing-")
        assert listing.agent_id == "agent-001"
        assert listing.reputation_score == 100.0

    def test_matches_query(self) -> None:
        listing = ServiceListing(
            title="Market Data Analysis",
            description="Professional data analysis services",
            service_type="data_analysis",
            tags=["market", "analysis", "data"],
        )
        assert listing.matches_query("market") is True
        assert listing.matches_query("data analysis") is True
        assert listing.matches_query("blockchain") is False

    def test_matches_capability(self) -> None:
        listing = ServiceListing(
            capabilities={"language": "zh", "domain": "finance"}
        )
        assert listing.matches_capability({"language": "zh"}) is True
        assert listing.matches_capability({"language": "en"}) is False
        assert listing.matches_capability({"domain": "finance"}) is True


class TestAgentMessage:
    def test_create_message(self) -> None:
        msg = AgentMessage(
            sender_id="agent-A",
            receiver_id="agent-B",
            message_type=MessageType.NEGOTIATION_OFFER,
            payload={"price": 100},
        )
        assert msg.message_id.startswith("msg-")
        assert msg.sender_id == "agent-A"

    def test_serialization_roundtrip(self) -> None:
        msg = AgentMessage(
            sender_id="agent-A",
            receiver_id="agent-B",
            message_type=MessageType.CONTRACT_PROPOSE,
            payload={"terms": {"price": 50}},
            references=["msg-001"],
        )
        data = msg.to_dict()
        restored = AgentMessage.from_dict(data)
        assert restored.sender_id == msg.sender_id
        assert restored.message_type == msg.message_type
        assert restored.payload == msg.payload


class TestNegotiationSession:
    def test_new_session(self) -> None:
        session = NegotiationSession(
            buyer_id="agent-buyer",
            seller_id="agent-seller",
        )
        assert session.current_round == 0
        assert session.status == NegotiationStatus.ACTIVE
        assert session.latest_offer is None

    def test_add_round(self) -> None:
        session = NegotiationSession(
            buyer_id="buyer",
            seller_id="seller",
        )
        terms = ContractTerms(price=100.0, deadline="2026-07-01T00:00:00Z")
        round_ = NegotiationRound(round_number=1, offer=terms, rationale="Initial offer")
        session.rounds.append(round_)
        assert session.current_round == 1
        assert session.latest_offer is not None
        assert session.latest_offer.price == 100.0

    def test_is_exhausted(self) -> None:
        session = NegotiationSession(max_rounds=3)
        terms = ContractTerms(price=50.0)
        for i in range(3):
            session.rounds.append(
                NegotiationRound(round_number=i + 1, offer=terms)
            )
        assert session.is_exhausted() is True


class TestRating:
    def test_overall_score(self) -> None:
        rating = Rating(
            rater_id="agent-A",
            transaction_id="txn-001",
            scores={"quality": 4.5, "timeliness": 5.0, "communication": 4.0},
        )
        assert rating.overall == 4.5

    def test_empty_scores(self) -> None:
        rating = Rating(rater_id="agent-A", transaction_id="txn-001")
        assert rating.overall == 0.0
