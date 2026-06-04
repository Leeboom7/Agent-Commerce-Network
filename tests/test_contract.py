"""Tests for contract manager."""

import pytest

from acp.contract.manager import ContractManager
from acp.protocol.models import ContractStatus, ContractTerms


class TestContractManager:
    @pytest.fixture
    def mgr(self) -> ContractManager:
        return ContractManager()

    @pytest.fixture
    def terms(self) -> ContractTerms:
        return ContractTerms(
            price=100.0,
            deadline="2026-07-01T00:00:00Z",
            deliverables=["report.md"],
            acceptance_criteria=["Must be in markdown format", "Must cite sources"],
            revision_rounds=2,
            penalty_rate=0.10,
        )

    def test_create_contract(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        assert contract.contract_id.startswith("contract-")
        assert contract.status == ContractStatus.DRAFT
        assert contract.buyer_id == "buyer-1"
        assert contract.seller_id == "seller-1"
        assert mgr.total_contracts == 1

    def test_sign_contract(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        mgr.sign(contract.contract_id, "buyer-1")
        mgr.sign(contract.contract_id, "seller-1")
        updated = mgr.get_contract(contract.contract_id)
        assert updated is not None
        assert updated.status == ContractStatus.ACTIVE

    def test_sign_wrong_party(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        with pytest.raises(ValueError, match="not a party"):
            mgr.sign(contract.contract_id, "random-agent")

    def test_deliver_and_accept(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        mgr.sign(contract.contract_id, "buyer-1")
        mgr.sign(contract.contract_id, "seller-1")

        # Seller delivers
        mgr.deliver(contract.contract_id, "seller-1", {"report": "# Report"})
        c = mgr.get_contract(contract.contract_id)
        assert c is not None and c.status == ContractStatus.DELIVERED

        # Buyer accepts
        mgr.accept(contract.contract_id, "buyer-1")
        c = mgr.get_contract(contract.contract_id)
        assert c is not None and c.status == ContractStatus.ACCEPTED
        assert c.fulfilled_at is not None

    def test_deliver_wrong_party(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        mgr.sign(contract.contract_id, "buyer-1")
        mgr.sign(contract.contract_id, "seller-1")

        with pytest.raises(ValueError, match="Only the seller"):
            mgr.deliver(contract.contract_id, "buyer-1", {})

    def test_reject_and_redeliver(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        mgr.sign(contract.contract_id, "buyer-1")
        mgr.sign(contract.contract_id, "seller-1")

        mgr.deliver(contract.contract_id, "seller-1", {"report": "bad"})
        mgr.reject(contract.contract_id, "buyer-1", "Quality insufficient")

        c = mgr.get_contract(contract.contract_id)
        assert c is not None and c.status == ContractStatus.REJECTED

        # Seller can re-deliver (REJECTED → DELIVERED transition allowed)
        mgr.deliver(contract.contract_id, "seller-1", {"report": "fixed"})
        c = mgr.get_contract(contract.contract_id)
        assert c is not None and c.status == ContractStatus.DELIVERED

    def test_dispute_and_resolve(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        mgr.sign(contract.contract_id, "buyer-1")
        mgr.sign(contract.contract_id, "seller-1")
        mgr.deliver(contract.contract_id, "seller-1", {"report": "maybe ok"})

        # Buyer disputes
        mgr.dispute(contract.contract_id, "buyer-1", "Report does not meet spec")
        c = mgr.get_contract(contract.contract_id)
        assert c is not None and c.status == ContractStatus.DISPUTED

        # Arbitrator resolves
        mgr.resolve(contract.contract_id, "arbitrator-1", {
            "verdict": "partial_refund", "refund_amount": 20.0
        })
        c = mgr.get_contract(contract.contract_id)
        assert c is not None and c.status == ContractStatus.RESOLVED

    def test_invalid_transition(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)

        # Can't accept a DRAFT contract
        with pytest.raises(ValueError, match="Invalid state transition"):
            mgr.accept(contract.contract_id, "buyer-1")

    def test_cancel(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        mgr.cancel(contract.contract_id, "buyer-1", "No longer needed")
        c = mgr.get_contract(contract.contract_id)
        assert c is not None and c.status == ContractStatus.CANCELLED

    def test_event_log(self, mgr: ContractManager, terms: ContractTerms) -> None:
        contract = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        mgr.sign(contract.contract_id, "buyer-1")

        events = mgr.get_events(contract.contract_id)
        assert len(events) == 2  # created + signed
        assert events[0].event_type == "created"
        assert events[1].event_type == "signed"

    def test_list_contracts(self, mgr: ContractManager, terms: ContractTerms) -> None:
        c1 = mgr.create_contract("buyer-1", "seller-1", "purchase", terms)
        mgr.create_contract("buyer-2", "seller-1", "commission", terms)

        all_c = mgr.list_contracts()
        assert len(all_c) == 2

        buyer1_c = mgr.list_contracts(agent_id="buyer-1")
        assert len(buyer1_c) == 1
        assert buyer1_c[0].contract_id == c1.contract_id

        seller1_c = mgr.list_contracts(agent_id="seller-1")
        assert len(seller1_c) == 2

    def test_get_agent_contracts(self, mgr: ContractManager, terms: ContractTerms) -> None:
        mgr.create_contract("agent-a", "agent-b", "purchase", terms)
        mgr.create_contract("agent-c", "agent-a", "purchase", terms)

        grouped = mgr.get_agent_contracts("agent-a")
        assert len(grouped["as_buyer"]) == 1
        assert len(grouped["as_seller"]) == 1

    def test_key_error_missing_contract(self, mgr: ContractManager) -> None:
        with pytest.raises(KeyError):
            mgr.get_contract("nonexistent")  # Will be None, not KeyError — fixed below
            mgr._get_contract("nonexistent")  # This one raises

    def test_get_nonexistent(self, mgr: ContractManager) -> None:
        assert mgr.get_contract("nonexistent") is None
        with pytest.raises(KeyError):
            mgr._get_contract("nonexistent")
