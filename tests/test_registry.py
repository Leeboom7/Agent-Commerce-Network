"""Tests for the Service Registry."""

import pytest

from acp.protocol.models import (
    PricingModel,
    PricingModelType,
    ServiceListing,
)
from acp.registry.registry import ServiceRegistry


class TestServiceRegistry:
    @pytest.fixture
    def registry(self) -> ServiceRegistry:
        return ServiceRegistry()

    @pytest.fixture
    def sample_listing(self) -> ServiceListing:
        return ServiceListing(
            agent_id="agent-data-001",
            service_type="data_analysis",
            economic_relationship="purchase",
            title="Market Data Analysis",
            description="Professional market data analysis with charts",
            capabilities={"language": "zh", "domain": "finance"},
            pricing=PricingModel(model_type=PricingModelType.FIXED, base_price=50.0),
            tags=["market", "analysis", "finance"],
        )

    def test_register_and_retrieve(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        lid = registry.register(sample_listing)
        retrieved = registry.get(lid)
        assert retrieved is not None
        assert retrieved.agent_id == "agent-data-001"
        assert retrieved.service_type == "data_analysis"

    def test_unregister(self, registry: ServiceRegistry, sample_listing: ServiceListing) -> None:
        lid = registry.register(sample_listing)
        assert registry.total_listings == 1
        removed = registry.unregister(lid)
        assert removed is True
        assert registry.total_listings == 0
        assert registry.get(lid) is None

    def test_unregister_agent(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        registry.register(sample_listing)
        listing2 = ServiceListing(
            agent_id="agent-data-001",
            service_type="report_writing",
            economic_relationship="commission",
            title="Report Writing",
        )
        registry.register(listing2)
        assert registry.total_listings == 2

        count = registry.unregister_agent("agent-data-001")
        assert count == 2
        assert registry.total_listings == 0

    def test_search_by_type(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        registry.register(sample_listing)
        results = registry.search(service_type="data_analysis")
        assert len(results) == 1
        assert results[0].listing.agent_id == "agent-data-001"

    def test_search_by_relationship(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        registry.register(sample_listing)
        results = registry.search(relationship_type="purchase")
        assert len(results) >= 1
        assert any(r.listing.economic_relationship == "purchase" for r in results)

    def test_search_by_query(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        registry.register(sample_listing)
        results = registry.search(query="market data")
        assert len(results) >= 1

    def test_search_no_match(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        registry.register(sample_listing)
        results = registry.search(query="blockchain")
        assert len(results) == 0

    def test_search_min_reputation(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        sample_listing.reputation_score = 30.0
        registry.register(sample_listing)
        results = registry.search(min_reputation=50.0)
        assert len(results) == 0

    def test_search_by_capability(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        registry.register(sample_listing)
        results = registry.search(required_capabilities={"language": "zh"})
        assert len(results) >= 1

        results = registry.search(required_capabilities={"language": "en"})
        assert len(results) == 0

    def test_search_by_tags(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        registry.register(sample_listing)
        results = registry.search(tags=["finance"])
        assert len(results) >= 1

        results = registry.search(tags=["blockchain"])
        assert len(results) == 0

    def test_discover_shortcut(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        registry.register(sample_listing)
        results = registry.discover("purchase")
        assert len(results) >= 1

    def test_ranking_by_reputation(
        self, registry: ServiceRegistry, sample_listing: ServiceListing
    ) -> None:
        sample_listing.reputation_score = 50.0  # Lower than elite
        registry.register(sample_listing)

        high_rep = ServiceListing(
            agent_id="agent-elite",
            service_type="data_analysis",
            economic_relationship="purchase",
            title="Elite Data Analysis",
        )
        high_rep.reputation_score = 95.0
        high_rep.total_transactions = 1000
        registry.register(high_rep)

        results = registry.search(service_type="data_analysis")
        assert len(results) >= 2
        # Higher reputation should rank first
        assert results[0].listing.agent_id == "agent-elite"

    def test_stats(self, registry: ServiceRegistry, sample_listing: ServiceListing) -> None:
        registry.register(sample_listing)
        stats = registry.get_stats()
        assert stats["total_listings"] == 1
        assert stats["total_agents"] == 1
