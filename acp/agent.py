"""
ACP — Base Agent Class.

Every agent in the commerce network extends or composes with this class.
Agents can register services, discover other agents, negotiate, contract,
and transact via the Agent Commerce Protocol.

Design principle: composition over inheritance. The BaseAgent provides
the minimal interface. Capabilities (negotiation strategies, verification
logic, etc.) are injected as composable components.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from acp.llm.qwen import QwenClient, QwenConfig
from acp.protocol.messaging import MessageBus, get_message_bus
from acp.protocol.models import (
    AgentIdentity,
    AgentMessage,
    MessageType,
    PricingModel,
    PricingModelType,
    ServiceListing,
)
from acp.registry.registry import ServiceRegistry


class BaseAgent(ABC):
    """
    Base class for all agents in the Agent Commerce Network.

    Provides:
    - Identity management
    - Service registration and discovery
    - Message sending/receiving
    - LLM access via Qwen Cloud

    Subclasses override execute() to implement domain-specific behavior.
    """

    def __init__(
        self,
        identity: AgentIdentity,
        registry: ServiceRegistry | None = None,
        message_bus: MessageBus | None = None,
        llm_client: QwenClient | None = None,
        llm_config: QwenConfig | None = None,
    ) -> None:
        self.identity = identity
        self.registry = registry or ServiceRegistry()
        self.bus = message_bus or get_message_bus()

        # LLM — share client when possible, create if needed
        if llm_client is not None:
            self.llm = llm_client
        else:
            try:
                self.llm = QwenClient(llm_config)
            except ValueError:
                self.llm = None  # Allows agent to run without LLM for testing

        # Register self on the message bus
        self.bus.register_agent(self.agent_id)

        # Owned service listings
        self._listings: dict[str, ServiceListing] = {}

    # ── Identity ───────────────────────────────────────────

    @property
    def agent_id(self) -> str:
        return self.identity.agent_id

    @property
    def name(self) -> str:
        return self.identity.name

    # ── Service Management ─────────────────────────────────

    def register_service(
        self,
        service_type: str,
        economic_relationship: str,
        title: str = "",
        description: str = "",
        capabilities: dict[str, Any] | None = None,
        pricing: PricingModel | None = None,
        tags: list[str] | None = None,
    ) -> ServiceListing:
        """
        Register a service that this agent offers on the commerce network.
        """
        if pricing is None:
            pricing = PricingModel(model_type=PricingModelType.NEGOTIABLE)

        listing = ServiceListing(
            agent_id=self.agent_id,
            service_type=service_type,
            economic_relationship=economic_relationship,
            title=title or f"{self.name} — {service_type}",
            description=description,
            capabilities=capabilities or {},
            pricing=pricing,
            tags=tags or [],
        )

        self.registry.register(listing)
        self._listings[listing.listing_id] = listing
        return listing

    def unregister_service(self, listing_id: str) -> bool:
        """Remove a service listing."""
        self._listings.pop(listing_id, None)
        return self.registry.unregister(listing_id)

    def get_my_listings(self) -> list[ServiceListing]:
        """Get all services registered by this agent."""
        return list(self._listings.values())

    # ── Discovery ──────────────────────────────────────────

    def discover_services(
        self,
        query: str = "",
        service_type: str | None = None,
        relationship_type: str | None = None,
        min_reputation: float = 0.0,
        required_capabilities: dict[str, Any] | None = None,
        limit: int = 10,
    ) -> list[Any]:
        """Search for services on the network."""
        return self.registry.search(
            query=query,
            service_type=service_type,
            relationship_type=relationship_type,
            min_reputation=min_reputation,
            required_capabilities=required_capabilities,
            limit=limit,
        )

    # ── Messaging ──────────────────────────────────────────

    async def send_message(
        self, receiver_id: str, msg_type: MessageType, payload: dict[str, Any],
        references: list[str] | None = None,
    ) -> AgentMessage | None:
        """Send a structured message to another agent."""
        msg = AgentMessage(
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_type=msg_type,
            payload=payload,
            references=references or [],
        )
        return await self.bus.send(msg)

    async def wait_for_message(
        self,
        msg_type: MessageType | None = None,
        timeout: float = 30.0,
    ) -> AgentMessage | None:
        """Wait for a message addressed to this agent."""
        return await self.bus.receive(self.agent_id, msg_type, timeout)

    def check_messages(self) -> list[AgentMessage]:
        """Check inbox without blocking."""
        return self.bus.get_inbox(self.agent_id)

    # ── Lifecycle ──────────────────────────────────────────

    @abstractmethod
    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a task. Override in subclasses.

        Args:
            task: A dictionary describing the task to perform.

        Returns:
            A dictionary with the task result.
        """
        raise NotImplementedError("Subclasses must implement execute()")

    async def shutdown(self) -> None:
        """Clean up resources. Override in subclasses if needed."""
        self.registry.unregister_agent(self.agent_id)
        self.bus.unregister_agent(self.agent_id)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.agent_id}, {self.name})>"
