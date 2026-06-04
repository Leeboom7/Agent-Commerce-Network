"""Tests for the Message Bus."""


import pytest

from acp.protocol.messaging import MessageBus, get_message_bus, reset_message_bus
from acp.protocol.models import AgentMessage, MessageType


class TestMessageBus:
    @pytest.fixture
    def bus(self) -> MessageBus:
        reset_message_bus()
        return MessageBus()

    def test_register_agent(self, bus: MessageBus) -> None:
        bus.register_agent("agent-1")
        assert bus.agent_count == 1

    def test_unregister_agent(self, bus: MessageBus) -> None:
        bus.register_agent("agent-1")
        bus.unregister_agent("agent-1")
        assert bus.agent_count == 0

    @pytest.mark.asyncio
    async def test_send_and_handler(self, bus: MessageBus) -> None:
        received_messages: list[AgentMessage] = []

        def handler(msg: AgentMessage) -> AgentMessage:
            received_messages.append(msg)
            return AgentMessage(
                sender_id="agent-2",
                receiver_id="agent-1",
                message_type=MessageType.ACKNOWLEDGMENT,
                payload={"status": "received"},
                references=[msg.message_id],
            )

        bus.register_handler("agent-2", MessageType.NEGOTIATION_OFFER, handler)

        msg = AgentMessage(
            sender_id="agent-1",
            receiver_id="agent-2",
            message_type=MessageType.NEGOTIATION_OFFER,
            payload={"price": 100},
        )

        response = await bus.send(msg)
        assert len(received_messages) == 1
        assert received_messages[0].payload == {"price": 100}
        assert response is not None
        assert response.message_type == MessageType.ACKNOWLEDGMENT

    @pytest.mark.asyncio
    async def test_send_no_handler(self, bus: MessageBus) -> None:
        msg = AgentMessage(
            sender_id="agent-1",
            receiver_id="agent-2",
            message_type=MessageType.SEARCH_REQUEST,
            payload={},
        )
        response = await bus.send(msg)
        assert response is None

    @pytest.mark.asyncio
    async def test_receive_message(self, bus: MessageBus) -> None:
        msg = AgentMessage(
            sender_id="agent-1",
            receiver_id="agent-2",
            message_type=MessageType.CONTRACT_PROPOSE,
            payload={"terms": {"price": 50}},
        )
        await bus.send(msg)

        received = await bus.receive("agent-2", timeout=0.5)
        assert received is not None
        assert received.sender_id == "agent-1"
        assert received.message_type == MessageType.CONTRACT_PROPOSE

    @pytest.mark.asyncio
    async def test_receive_filtered(self, bus: MessageBus) -> None:
        await bus.send(AgentMessage(
            sender_id="agent-1", receiver_id="agent-3",
            message_type=MessageType.SEARCH_REQUEST, payload={},
        ))
        await bus.send(AgentMessage(
            sender_id="agent-2", receiver_id="agent-3",
            message_type=MessageType.CONTRACT_SIGN, payload={},
        ))

        received = await bus.receive("agent-3", MessageType.CONTRACT_SIGN, timeout=0.5)
        assert received is not None
        assert received.message_type == MessageType.CONTRACT_SIGN

    @pytest.mark.asyncio
    async def test_receive_timeout(self, bus: MessageBus) -> None:
        received = await bus.receive("agent-empty", timeout=0.1)
        assert received is None

    def test_inbox(self, bus: MessageBus) -> None:
        assert bus.queue_depth == 0
        bus._inboxes["agent-1"].append(
            AgentMessage(sender_id="agent-2", receiver_id="agent-1",
                         message_type=MessageType.ACKNOWLEDGMENT, payload={})
        )
        assert bus.queue_depth == 1
        inbox = bus.get_inbox("agent-1")
        assert len(inbox) == 1
        bus.clear_inbox("agent-1")
        assert bus.queue_depth == 0

    def test_global_bus_singleton(self) -> None:
        reset_message_bus()
        bus1 = get_message_bus()
        bus2 = get_message_bus()
        assert bus1 is bus2
