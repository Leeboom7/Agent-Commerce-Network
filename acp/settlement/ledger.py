"""
ACP Settlement Ledger.

Credit system for the open-source (MVP) edition.
Tracks agent balances, processes transfers, and maintains
an immutable transaction history.

In the production edition, this is replaced by blockchain-based
settlement with stablecoin support.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from typing import Any


class TransactionLedger:
    """
    Credit-based settlement ledger for the Agent Commerce Network.

    Features:
    - Initial balance allocation for new agents
    - Transfer between agents
    - Immutable transaction history
    - Balance queries
    - Audit trail
    """

    def __init__(self, initial_balance: float = 1000.0) -> None:
        self.initial_balance = initial_balance
        # agent_id → current balance
        self._balances: dict[str, float] = defaultdict(lambda: initial_balance)
        # Complete transaction history
        self._transactions: list[dict[str, Any]] = []
        # Agent-specific transaction lists (for fast lookup)
        self._agent_txns: dict[str, list[int]] = defaultdict(list)

    # ── Balance Management ────────────────────────────────

    def get_balance(self, agent_id: str) -> float:
        """Get current balance for an agent."""
        return self._balances.get(agent_id, self.initial_balance)

    def set_initial_balance(self, agent_id: str, amount: float) -> None:
        """Set a custom initial balance for a new agent."""
        if agent_id in self._balances:
            raise ValueError(
                f"Agent {agent_id} already has a balance. Use transfer() instead."
            )
        self._balances[agent_id] = amount

    # ── Transfers ─────────────────────────────────────────

    def transfer(
        self,
        from_agent: str,
        to_agent: str,
        amount: float,
        contract_id: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        """
        Transfer credits from one agent to another.

        Returns the transaction record.
        Raises ValueError if insufficient balance.
        """
        if amount <= 0:
            raise ValueError(f"Transfer amount must be positive, got {amount}")

        from_balance = self.get_balance(from_agent)
        if from_balance < amount:
            raise ValueError(
                f"Insufficient balance: {from_agent} has {from_balance:.2f} NC, "
                f"tried to transfer {amount:.2f} NC"
            )

        # Execute transfer
        self._balances[from_agent] = from_balance - amount
        self._balances[to_agent] = self.get_balance(to_agent) + amount

        # Record transaction
        txn = {
            "transaction_id": f"txn-{len(self._transactions) + 1:06d}",
            "from_agent": from_agent,
            "to_agent": to_agent,
            "amount": amount,
            "currency": "NC",
            "contract_id": contract_id,
            "reason": reason,
            "timestamp": datetime.now(UTC).isoformat(),
            "from_balance_after": self._balances[from_agent],
            "to_balance_after": self._balances[to_agent],
        }
        txn_index = len(self._transactions)
        self._transactions.append(txn)
        self._agent_txns[from_agent].append(txn_index)
        self._agent_txns[to_agent].append(txn_index)

        return txn

    def transfer_with_penalty(
        self,
        from_agent: str,
        to_agent: str,
        contract_amount: float,
        penalty_rate: float,
        contract_id: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        """
        Transfer with penalty deduction (for failed deliveries).
        Penalty is burned (removed from circulation).
        """
        penalty = contract_amount * penalty_rate
        net_amount = contract_amount - penalty

        # Transfer net amount to seller
        result = self.transfer(
            from_agent=from_agent,
            to_agent=to_agent,
            amount=net_amount,
            contract_id=contract_id,
            reason=f"{reason} (penalty: {penalty:.2f} NC, {penalty_rate*100:.0f}%)",
        )

        # Burn penalty
        self._balances[from_agent] -= penalty

        return {**result, "penalty": penalty, "net_amount": net_amount}

    # ── History & Audit ───────────────────────────────────

    def get_transaction(self, txn_id: str) -> dict[str, Any] | None:
        """Get a transaction by ID."""
        for txn in self._transactions:
            if txn["transaction_id"] == txn_id:
                return txn
        return None

    def get_history(
        self,
        agent_id: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Get transaction history, optionally filtered by agent."""
        if agent_id:
            indices = self._agent_txns.get(agent_id, [])
            txns = [self._transactions[i] for i in reversed(indices)]
        else:
            txns = list(reversed(self._transactions))

        return txns[offset:offset + limit]

    def get_volume(self, agent_id: str) -> dict[str, float]:
        """Get total sent and received volume for an agent."""
        sent = 0.0
        received = 0.0
        for i in self._agent_txns.get(agent_id, []):
            txn = self._transactions[i]
            if txn["from_agent"] == agent_id:
                sent += txn["amount"]
            if txn["to_agent"] == agent_id:
                received += txn["amount"]

        return {"sent": round(sent, 2), "received": round(received, 2)}

    # ── Stats ─────────────────────────────────────────────

    @property
    def total_transactions(self) -> int:
        return len(self._transactions)

    @property
    def total_agents(self) -> int:
        return len(self._balances)

    def get_stats(self) -> dict[str, Any]:
        """Get ledger statistics."""
        all_balances = list(self._balances.values())
        total_supply = sum(all_balances) if all_balances else 0
        return {
            "total_transactions": self.total_transactions,
            "total_agents": self.total_agents,
            "total_credit_supply": round(total_supply, 2),
            "average_balance": round(total_supply / max(1, len(all_balances)), 2),
            "max_balance": round(max(all_balances), 2) if all_balances else 0,
            "min_balance": round(min(all_balances), 2) if all_balances else 0,
        }
