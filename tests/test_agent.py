"""Tests for the BaseAgent class."""

import pytest

from acp.agent import BaseAgent
from acp.protocol.messaging import reset_message_bus
from acp.protocol.models import AgentIdentity, PricingModel, PricingModelType
from acp.registry.registry import ServiceRegistry


class _ConcreteAgent(BaseAgent):
    """Concrete agent for testing (not collected by pytest)."""

    async def execute(self, task: dict) -> dict:
        return {"status": "done", "task": task}


class TestBaseAgent:
    @pytest.fixture(autouse=True)
    def reset(self) -> None:
        reset_message_bus()

    @pytest.fixture
    def registry(self) -> ServiceRegistry:
        return ServiceRegistry()

    @pytest.fixture
    def agent(self, registry: ServiceRegistry) -> _ConcreteAgent:
        identity = AgentIdentity.create("TestAgent", "A test agent")
        return _ConcreteAgent(identity=identity, registry=registry)

    def test_identity(self, agent: _ConcreteAgent) -> None:
        assert agent.name == "TestAgent"
        assert agent.agent_id.startswith("agent-")

    def test_register_service(self, agent: _ConcreteAgent) -> None:
        listing = agent.register_service(
            service_type="data_analysis",
            economic_relationship="purchase",
            title="Data Analysis Service",
            description="I analyze data",
            capabilities={"language": "zh"},
            pricing=PricingModel(model_type=PricingModelType.FIXED, base_price=50.0),
            tags=["analysis"],
        )
        assert listing.agent_id == agent.agent_id
        assert listing.service_type == "data_analysis"

        # Should be in registry
        results = agent.discover_services(service_type="data_analysis")
        assert len(results) == 1

    def test_unregister_service(self, agent: _ConcreteAgent) -> None:
        listing = agent.register_service(
            service_type="report_writing",
            economic_relationship="commission",
            title="Report Writing",
        )
        assert len(agent.get_my_listings()) == 1

        removed = agent.unregister_service(listing.listing_id)
        assert removed is True
        assert len(agent.get_my_listings()) == 0

    def test_discover_services(self, agent: _ConcreteAgent) -> None:
        # Register another agent's service in the same registry
        from acp.protocol.models import ServiceListing

        other_listing = ServiceListing(
            agent_id="other-agent",
            service_type="translation",
            economic_relationship="purchase",
            title="Translation Service",
            tags=["language", "translation"],
        )
        agent.registry.register(other_listing)

        results = agent.discover_services(service_type="translation")
        assert len(results) == 1
        assert results[0].listing.agent_id == "other-agent"

    def test_get_my_listings(self, agent: _ConcreteAgent) -> None:
        agent.register_service("a", "purchase", title="Service A")
        agent.register_service("b", "commission", title="Service B")
        assert len(agent.get_my_listings()) == 2

    @pytest.mark.asyncio
    async def test_execute(self, agent: _ConcreteAgent) -> None:
        result = await agent.execute({"action": "test"})
        assert result["status"] == "done"

    @pytest.mark.asyncio
    async def test_shutdown(self, agent: _ConcreteAgent) -> None:
        agent.register_service("test", "purchase", title="Test")
        assert agent.registry.total_listings == 1
        await agent.shutdown()
        assert agent.registry.total_listings == 0
