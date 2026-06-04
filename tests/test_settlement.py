"""Tests for settlement ledger."""

import pytest

from acp.settlement.ledger import TransactionLedger


class TestTransactionLedger:
    @pytest.fixture
    def ledger(self) -> TransactionLedger:
        return TransactionLedger(initial_balance=1000.0)

    def test_initial_balance(self, ledger: TransactionLedger) -> None:
        assert ledger.get_balance("new-agent") == 1000.0

    def test_set_initial_balance(self, ledger: TransactionLedger) -> None:
        ledger.set_initial_balance("special-agent", 5000.0)
        assert ledger.get_balance("special-agent") == 5000.0

    def test_cannot_reset_balance(self, ledger: TransactionLedger) -> None:
        ledger.set_initial_balance("agent-x", 2000.0)
        with pytest.raises(ValueError, match="already has a balance"):
            ledger.set_initial_balance("agent-x", 3000.0)

    def test_transfer(self, ledger: TransactionLedger) -> None:
        txn = ledger.transfer("buyer", "seller", 100.0, "contract-1", "Payment for report")
        assert txn["from_agent"] == "buyer"
        assert txn["to_agent"] == "seller"
        assert txn["amount"] == 100.0
        assert ledger.get_balance("buyer") == 900.0
        assert ledger.get_balance("seller") == 1100.0

    def test_transfer_insufficient_balance(self, ledger: TransactionLedger) -> None:
        with pytest.raises(ValueError, match="Insufficient balance"):
            ledger.transfer("buyer", "seller", 2000.0)

    def test_transfer_negative_amount(self, ledger: TransactionLedger) -> None:
        with pytest.raises(ValueError, match="must be positive"):
            ledger.transfer("buyer", "seller", -50.0)

    def test_transfer_with_penalty(self, ledger: TransactionLedger) -> None:
        """10% penalty on 100 NC = 10 NC burned, seller gets 90 NC."""
        result = ledger.transfer_with_penalty(
            "buyer", "seller", 100.0, 0.10, "contract-1",
            "Quality deduction"
        )
        assert result["penalty"] == 10.0
        assert result["net_amount"] == 90.0
        # Buyer: 1000 - 90 (to seller as net) - 10 (penalty: burned separately) = 900
        # The penalty is additionally deducted from the buyer after the transfer
        assert ledger.get_balance("buyer") == 900.0
        assert ledger.get_balance("seller") == 1090.0

    def test_transaction_history(self, ledger: TransactionLedger) -> None:
        ledger.transfer("a", "b", 50.0, reason="first")
        ledger.transfer("b", "c", 30.0, reason="second")
        ledger.transfer("a", "c", 20.0, reason="third")

        assert ledger.total_transactions == 3

        a_history = ledger.get_history(agent_id="a")
        assert len(a_history) == 2  # a sent to b and c

        b_history = ledger.get_history(agent_id="b")
        assert len(b_history) == 2  # b received from a, sent to c

        # Full history (no filter)
        all_history = ledger.get_history()
        assert len(all_history) == 3

    def test_get_transaction_by_id(self, ledger: TransactionLedger) -> None:
        txn = ledger.transfer("a", "b", 50.0)
        found = ledger.get_transaction(txn["transaction_id"])
        assert found is not None
        assert found["amount"] == 50.0

    def test_get_volume(self, ledger: TransactionLedger) -> None:
        ledger.transfer("agent-x", "agent-y", 100.0)
        ledger.transfer("agent-y", "agent-x", 50.0)
        ledger.transfer("agent-z", "agent-x", 200.0)

        vol_x = ledger.get_volume("agent-x")
        assert vol_x["sent"] == 100.0
        assert vol_x["received"] == 250.0

        vol_y = ledger.get_volume("agent-y")
        assert vol_y["sent"] == 50.0
        assert vol_y["received"] == 100.0

    def test_stats(self, ledger: TransactionLedger) -> None:
        ledger.transfer("a", "b", 100.0)
        ledger.transfer("a", "c", 200.0)

        stats = ledger.get_stats()
        assert stats["total_transactions"] == 2
        assert stats["total_agents"] == 3  # a, b, c
        assert stats["total_credit_supply"] == 3000.0  # 3 * 1000

    def test_history_pagination(self, ledger: TransactionLedger) -> None:
        for i in range(10):
            ledger.transfer("a", "b", 10.0, reason=f"txn-{i}")

        page = ledger.get_history(agent_id="a", limit=5, offset=0)
        assert len(page) == 5

        page2 = ledger.get_history(agent_id="a", limit=5, offset=5)
        assert len(page2) == 5
