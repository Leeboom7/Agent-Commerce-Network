"""
ACP Contract Manager.

Manages the full lifecycle of service contracts between agents:
draft → active → delivered → accepted/disputed → resolved.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from acp.protocol.models import (
    ContractStatus,
    ContractTerms,
    ServiceContract,
)


# ──────────────────────────────────────────────────────────────
# Contract Event Log
# ──────────────────────────────────────────────────────────────


@dataclass
class ContractEvent:
    """An event in a contract's lifecycle."""

    event_id: str = field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:12]}")
    contract_id: str = ""
    event_type: str = ""  # "created", "signed", "delivered", "accepted", etc.
    actor_id: str = ""  # Which agent triggered this event
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ──────────────────────────────────────────────────────────────
# Contract Manager
# ──────────────────────────────────────────────────────────────


class ContractManager:
    """
    Manages the lifecycle of service contracts.

    Enforces valid state transitions and maintains an immutable
    event log for auditability.
    """

    # Valid state transitions
    VALID_TRANSITIONS: dict[ContractStatus, set[ContractStatus]] = {
        ContractStatus.DRAFT: {ContractStatus.ACTIVE, ContractStatus.CANCELLED},
        ContractStatus.ACTIVE: {
            ContractStatus.DELIVERED,
            ContractStatus.DISPUTED,
            ContractStatus.CANCELLED,
        },
        ContractStatus.DELIVERED: {
            ContractStatus.ACCEPTED,
            ContractStatus.REJECTED,
            ContractStatus.DISPUTED,
        },
        ContractStatus.REJECTED: {ContractStatus.DELIVERED, ContractStatus.DISPUTED},
        ContractStatus.DISPUTED: {ContractStatus.RESOLVED, ContractStatus.CANCELLED},
        ContractStatus.RESOLVED: set(),  # Terminal
        ContractStatus.ACCEPTED: set(),  # Terminal
        ContractStatus.CANCELLED: set(),  # Terminal
    }

    def __init__(self) -> None:
        self._contracts: dict[str, ServiceContract] = {}
        self._events: dict[str, list[ContractEvent]] = {}

    # ── Contract Creation ──────────────────────────────────

    def create_contract(
        self,
        buyer_id: str,
        seller_id: str,
        relationship_type: str,
        terms: ContractTerms,
        negotiation_session_id: str | None = None,
    ) -> ServiceContract:
        """
        Create a new contract in DRAFT status.

        Typically called after a successful negotiation.
        """
        contract = ServiceContract(
            contract_id=f"contract-{uuid.uuid4().hex[:12]}",
            parties=[buyer_id, seller_id],
            relationship_type=relationship_type,
            terms=terms,
            status=ContractStatus.DRAFT,
            negotiation_session_id=negotiation_session_id,
        )
        self._contracts[contract.contract_id] = contract
        self._record_event(contract.contract_id, "created", buyer_id)
        return contract

    # ── Contract Operations ────────────────────────────────

    def sign(self, contract_id: str, signer_id: str) -> ServiceContract:
        """
        Sign a contract, moving it to ACTIVE when all parties have signed.

        In MVP mode, the contract becomes ACTIVE when both parties sign.
        The first sign keeps it DRAFT; the second sign activates it.
        """
        contract = self._get_contract(contract_id)

        # Only validate transition when moving from DRAFT to ACTIVE
        if contract.status == ContractStatus.DRAFT:
            self._validate_transition(contract, ContractStatus.ACTIVE)

        # Check that signer is a party to the contract
        if signer_id not in contract.parties:
            raise ValueError(f"Signer {signer_id} is not a party to contract {contract_id}")

        # Track who has signed (simple MVP: activate on second sign)
        if not hasattr(contract, '_signatures'):
            contract._signatures: list[str] = []  # type: ignore[attr-defined]

        if signer_id in getattr(contract, '_signatures', []):
            raise ValueError(f"Signer {signer_id} has already signed contract {contract_id}")

        contract._signatures.append(signer_id)  # type: ignore[attr-defined]

        # Activate when both parties have signed
        if len(contract._signatures) >= 2:  # type: ignore[attr-defined]
            contract.status = ContractStatus.ACTIVE

        self._record_event(contract_id, "signed", signer_id)
        return contract

    def deliver(
        self, contract_id: str, seller_id: str, delivery: dict[str, Any]
    ) -> ServiceContract:
        """
        Record a delivery by the seller. Moves to DELIVERED status.

        Args:
            delivery: The actual deliverable (data, report, etc.).
        """
        contract = self._get_contract(contract_id)
        self._validate_transition(contract, ContractStatus.DELIVERED)

        if seller_id != contract.seller_id:
            raise ValueError(f"Only the seller ({contract.seller_id}) can deliver")

        contract.delivery_attempts.append({
            "attempt": len(contract.delivery_attempts) + 1,
            "delivery": delivery,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        contract.status = ContractStatus.DELIVERED
        self._record_event(contract_id, "delivered", seller_id, {"delivery": delivery})
        return contract

    def accept(self, contract_id: str, buyer_id: str) -> ServiceContract:
        """Buyer accepts the delivery. Terminal state."""
        contract = self._get_contract(contract_id)
        self._validate_transition(contract, ContractStatus.ACCEPTED)

        if buyer_id != contract.buyer_id:
            raise ValueError(f"Only the buyer ({contract.buyer_id}) can accept")

        contract.status = ContractStatus.ACCEPTED
        contract.fulfilled_at = datetime.now(timezone.utc)
        self._record_event(contract_id, "accepted", buyer_id)
        return contract

    def reject(self, contract_id: str, buyer_id: str, reason: str) -> ServiceContract:
        """
        Buyer rejects the delivery. Contract returns to DELIVERED
        after seller revises (seller calls deliver() again).
        """
        contract = self._get_contract(contract_id)
        self._validate_transition(contract, ContractStatus.REJECTED)

        if buyer_id != contract.buyer_id:
            raise ValueError(f"Only the buyer ({contract.buyer_id}) can reject")

        contract.status = ContractStatus.REJECTED
        self._record_event(contract_id, "rejected", buyer_id, {"reason": reason})
        return contract

    def dispute(
        self, contract_id: str, disputer_id: str, claim: str
    ) -> ServiceContract:
        """Either party files a dispute. Moves to DISPUTED status."""
        contract = self._get_contract(contract_id)
        self._validate_transition(contract, ContractStatus.DISPUTED)

        contract.status = ContractStatus.DISPUTED
        self._record_event(
            contract_id, "disputed", disputer_id, {"claim": claim}
        )
        return contract

    def resolve(self, contract_id: str, resolver_id: str, resolution: dict[str, Any]) -> ServiceContract:
        """
        Resolve a disputed contract. Typically called by an arbitrator agent.
        Moves to RESOLVED (terminal).
        """
        contract = self._get_contract(contract_id)
        self._validate_transition(contract, ContractStatus.RESOLVED)

        contract.status = ContractStatus.RESOLVED
        contract.fulfilled_at = datetime.now(timezone.utc)
        self._record_event(
            contract_id, "resolved", resolver_id, {"resolution": resolution}
        )
        return contract

    def cancel(self, contract_id: str, canceller_id: str, reason: str = "") -> ServiceContract:
        """Cancel a contract. Terminal state."""
        contract = self._get_contract(contract_id)
        self._validate_transition(contract, ContractStatus.CANCELLED)

        contract.status = ContractStatus.CANCELLED
        self._record_event(
            contract_id, "cancelled", canceller_id, {"reason": reason}
        )
        return contract

    # ── Query ──────────────────────────────────────────────

    def get_contract(self, contract_id: str) -> ServiceContract | None:
        return self._contracts.get(contract_id)

    def get_events(self, contract_id: str) -> list[ContractEvent]:
        return list(self._events.get(contract_id, []))

    def list_contracts(
        self,
        agent_id: str | None = None,
        status: ContractStatus | None = None,
    ) -> list[ServiceContract]:
        """List contracts, optionally filtered by agent and/or status."""
        results = list(self._contracts.values())

        if agent_id:
            results = [c for c in results if agent_id in c.parties]

        if status:
            results = [c for c in results if c.status == status]

        return sorted(results, key=lambda c: c.created_at, reverse=True)

    def get_agent_contracts(self, agent_id: str) -> dict[str, list[ServiceContract]]:
        """Get all contracts for an agent, grouped by status."""
        grouped: dict[str, list[ServiceContract]] = {
            "as_buyer": [],
            "as_seller": [],
        }
        for contract in self._contracts.values():
            if contract.buyer_id == agent_id:
                grouped["as_buyer"].append(contract)
            elif contract.seller_id == agent_id:
                grouped["as_seller"].append(contract)
        return grouped

    # ── Helpers ────────────────────────────────────────────

    def _get_contract(self, contract_id: str) -> ServiceContract:
        contract = self._contracts.get(contract_id)
        if contract is None:
            raise KeyError(f"Contract not found: {contract_id}")
        return contract

    def _validate_transition(
        self, contract: ServiceContract, target: ContractStatus
    ) -> None:
        valid = self.VALID_TRANSITIONS.get(contract.status, set())
        if target not in valid:
            raise ValueError(
                f"Invalid state transition: {contract.status.value} → {target.value}. "
                f"Valid transitions: {[s.value for s in valid]}"
            )

    def _record_event(
        self,
        contract_id: str,
        event_type: str,
        actor_id: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        event = ContractEvent(
            contract_id=contract_id,
            event_type=event_type,
            actor_id=actor_id,
            details=details or {},
        )
        if contract_id not in self._events:
            self._events[contract_id] = []
        self._events[contract_id].append(event)

    @property
    def total_contracts(self) -> int:
        return len(self._contracts)
