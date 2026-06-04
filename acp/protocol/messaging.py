"""
ACP Protocol — Message Bus.

The communication infrastructure that agents use to send structured
messages to each other. Supports in-memory (MVP) and Redis-backed
(production) transports.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Callable
from typing import Any

from acp.protocol.models import AgentMessage, MessageType

# ──────────────────────────────────────────────────────────────
# Message Handler Type
# ──────────────────────────────────────────────────────────────

MessageHandler = Callable[[AgentMessage], Any]
"""A function that processes an incoming message and optionally returns a response."""


# ──────────────────────────────────────────────────────────────
# In-Memory Message Bus (MVP)
# ──────────────────────────────────────────────────────────────


class MessageBus:
    """
    In-memory message bus for agent-to-agent communication.

    Agents register handlers for specific message types. When a message
    is sent, the bus routes it to the receiver's registered handler.

    This is the MVP implementation. For production, replace with
    Redis Pub/Sub or a dedicated message queue.
    """

    def __init__(self) -> None:
        # agent_id -> {message_type -> handler}
        self._handlers: dict[str, dict[MessageType, MessageHandler]] = defaultdict(dict)
        # agent_id -> list of messages (inbox)
        self._inboxes: dict[str, list[AgentMessage]] = defaultdict(list)
        # message_id -> response message
        self._responses: dict[str, AgentMessage] = {}
        # Event for notifying agents of new messages
        self._events: dict[str, asyncio.Event] = defaultdict(asyncio.Event)

    # ── Registration ──────────────────────────────────────

    def register_agent(self, agent_id: str) -> None:
        """Register an agent on the bus."""
        if agent_id not in self._inboxes:
            self._inboxes[agent_id] = []

    def register_handler(
        self, agent_id: str, message_type: MessageType, handler: MessageHandler
    ) -> None:
        """Register a handler for a specific message type."""
        self.register_agent(agent_id)
        self._handlers[agent_id][message_type] = handler

    def unregister_agent(self, agent_id: str) -> None:
        """Remove an agent from the bus."""
        self._handlers.pop(agent_id, None)
        self._inboxes.pop(agent_id, None)
        self._events.pop(agent_id, None)

    # ── Sending ───────────────────────────────────────────

    async def send(self, message: AgentMessage) -> AgentMessage | None:
        """
        Send a message to a receiver agent.

        If the receiver has a handler registered for this message type,
        the handler is invoked synchronously (within the same call) and
        the response is returned.

        The message is also stored in the receiver's inbox regardless.
        """
        receiver_id = message.receiver_id
        msg_type = message.message_type

        # Store in inbox
        self._inboxes[receiver_id].append(message)

        # Signal waiting consumers
        if receiver_id in self._events:
            self._events[receiver_id].set()

        # If handler registered, invoke it
        handler = self._handlers.get(receiver_id, {}).get(msg_type)
        if handler is not None:
            try:
                response = handler(message)
                if isinstance(response, AgentMessage):
                    self._responses[message.message_id] = response
                    return response
            except Exception:
                # Handler errors should not crash the bus
                error_msg = AgentMessage(
                    sender_id="system",
                    receiver_id=message.sender_id,
                    message_type=MessageType.ERROR,
                    payload={"original_message_id": message.message_id,
                             "error": "Handler execution failed"},
                )
                return error_msg

        return None

    async def send_and_wait(
        self, message: AgentMessage, timeout: float = 30.0
    ) -> AgentMessage | None:
        """Send a message and wait for a response, with timeout."""
        response = await self.send(message)
        if response is not None:
            return response

        # Wait for async response in inbox
        try:
            event = self._events.get(message.sender_id, asyncio.Event())
            event.clear()
            await asyncio.wait_for(event.wait(), timeout=timeout)

            # Check inbox for response
            inbox = self._inboxes[message.sender_id]
            for msg in reversed(inbox):
                if (msg.message_type in (MessageType.ACKNOWLEDGMENT, MessageType.ERROR)
                        and message.message_id in msg.references):
                    return msg
        except TimeoutError:
            pass

        return None

    # ── Receiving ─────────────────────────────────────────

    async def receive(
        self, agent_id: str, message_type: MessageType | None = None, timeout: float = 10.0
    ) -> AgentMessage | None:
        """
        Wait for and retrieve the next message for an agent.

        If message_type is specified, only returns messages of that type.
        """
        deadline = asyncio.get_event_loop().time() + timeout

        while asyncio.get_event_loop().time() < deadline:
            # Check existing inbox
            inbox = self._inboxes[agent_id]
            for i, msg in enumerate(inbox):
                if message_type is None or msg.message_type == message_type:
                    return inbox.pop(i)

            # Wait for new messages
            remaining = deadline - asyncio.get_event_loop().time()
            if remaining > 0:
                event = self._events[agent_id]
                event.clear()
                try:
                    await asyncio.wait_for(event.wait(), timeout=remaining)
                except TimeoutError:
                    return None

        return None

    def get_inbox(self, agent_id: str) -> list[AgentMessage]:
        """Get all messages in an agent's inbox (non-blocking)."""
        return list(self._inboxes.get(agent_id, []))

    def clear_inbox(self, agent_id: str) -> None:
        """Clear an agent's inbox."""
        self._inboxes[agent_id] = []

    # ── Utility ───────────────────────────────────────────

    def get_response(self, message_id: str) -> AgentMessage | None:
        """Get a stored response for a message."""
        return self._responses.get(message_id)

    @property
    def agent_count(self) -> int:
        return len(self._inboxes)

    @property
    def queue_depth(self) -> int:
        return sum(len(inbox) for inbox in self._inboxes.values())


# ──────────────────────────────────────────────────────────────
# Global Bus Instance (for convenience in single-process usage)
# ──────────────────────────────────────────────────────────────

_default_bus: MessageBus | None = None


def get_message_bus() -> MessageBus:
    """Get or create the default message bus instance."""
    global _default_bus
    if _default_bus is None:
        _default_bus = MessageBus()
    return _default_bus


def reset_message_bus() -> None:
    """Reset the default message bus (useful in tests)."""
    global _default_bus
    _default_bus = None
