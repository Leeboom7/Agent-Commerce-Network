"""Tests for arbitration engine."""

import pytest

from acp.arbitration.arbitrator import ArbitrationEngine, RulingType
from acp.protocol.models import (
    CheckResult,
    ContractStatus,
    ContractTerms,
    ServiceContract,
    VerificationReport,
)


class TestArbitrationEngine:
    @pytest.fixture
    def engine(self) -> ArbitrationEngine:
        return ArbitrationEngine()

    @pytest.fixture
    def contract(self) -> ServiceContract:
        return ServiceContract(
            contract_id="contract-test-1",
            parties=["buyer-1", "seller-1"],
            relationship_type="purchase",
            terms=ContractTerms(price=100.0),
            status=ContractStatus.ACTIVE,
        )

    def test_file_case(self, engine: ArbitrationEngine, contract: ServiceContract) -> None:
        case = engine.file_case(contract, "buyer-1", "Seller didn't deliver on time")
        assert case.case_id.startswith("case-")
        assert case.claimant_id == "buyer-1"
        assert case.respondent_id == "seller-1"
        assert engine.total_cases == 1

    def test_file_case_as_seller(self, engine: ArbitrationEngine, contract: ServiceContract) -> None:
        case = engine.file_case(contract, "seller-1", "Buyer refuses to accept delivery")
        assert case.claimant_id == "seller-1"
        assert case.respondent_id == "buyer-1"

    def test_rule_buyer_upheld_with_failed_verification(
        self, engine: ArbitrationEngine, contract: ServiceContract
    ) -> None:
        contract.status = ContractStatus.DELIVERED
        vr = VerificationReport(
            contract_id=contract.contract_id,
            verifier_id="v-1",
            checks=[
                CheckResult(criterion="Accuracy", passed=False, notes="Data is wrong"),
                CheckResult(criterion="Completeness", passed=False, notes="Missing sections"),
            ],
            verdict="rejected",
            summary="All criteria failed",
        )

        case = engine.file_case(contract, "buyer-1", "Quality is terrible",
                               verification_report=vr)
        ruling = engine.rule(case.case_id, "arb-1", contract)

        assert ruling.ruling_type == RulingType.BUYER_UPHELD
        assert ruling.remedy["action"] == "refund"

    def test_rule_seller_upheld_with_passing_verification(
        self, engine: ArbitrationEngine, contract: ServiceContract
    ) -> None:
        contract.status = ContractStatus.DELIVERED
        vr = VerificationReport(
            contract_id=contract.contract_id,
            verifier_id="v-1",
            checks=[
                CheckResult(criterion="Format", passed=True),
                CheckResult(criterion="Content", passed=True),
            ],
            verdict="accepted",
            summary="All passed",
        )

        case = engine.file_case(contract, "buyer-1", "I don't like the quality",
                               verification_report=vr)
        ruling = engine.rule(case.case_id, "arb-1", contract)

        assert ruling.ruling_type == RulingType.SELLER_UPHELD
        assert ruling.remedy["action"] == "no_refund"

    def test_rule_split_on_partial_verification(
        self, engine: ArbitrationEngine, contract: ServiceContract
    ) -> None:
        contract.status = ContractStatus.DELIVERED
        vr = VerificationReport(
            contract_id=contract.contract_id,
            verifier_id="v-1",
            checks=[
                CheckResult(criterion="Format", passed=True),
                CheckResult(criterion="Content", passed=False, notes="Minor issues"),
            ],
            verdict="partial",
            summary="1 of 2 failed",
        )

        case = engine.file_case(contract, "buyer-1", "Partially acceptable",
                               verification_report=vr)
        ruling = engine.rule(case.case_id, "arb-1", contract)

        assert ruling.ruling_type == RulingType.SPLIT
        assert ruling.remedy["action"] == "seller_must_revise"

    def test_rule_late_delivery(self, engine: ArbitrationEngine, contract: ServiceContract) -> None:
        # Contract is still active (seller hasn't delivered)
        case = engine.file_case(contract, "buyer-1", "Seller is late, delivery overdue by 3 days")
        ruling = engine.rule(case.case_id, "arb-1", contract)

        assert ruling.ruling_type == RulingType.BUYER_UPHELD
        assert ruling.remedy["action"] == "refund"

    def test_rule_delivered_without_verification(
        self, engine: ArbitrationEngine, contract: ServiceContract
    ) -> None:
        contract.status = ContractStatus.DELIVERED
        case = engine.file_case(contract, "buyer-1", "Quality is questionable")
        ruling = engine.rule(case.case_id, "arb-1", contract)

        assert ruling.ruling_type == RulingType.SPLIT

    def test_get_case_and_ruling(
        self, engine: ArbitrationEngine, contract: ServiceContract
    ) -> None:
        vr = VerificationReport(
            contract_id=contract.contract_id,
            verifier_id="v-1",
            checks=[CheckResult(criterion="Test", passed=True)],
            verdict="accepted",
        )
        contract.status = ContractStatus.DELIVERED

        case = engine.file_case(contract, "buyer-1", "test", verification_report=vr)
        ruling = engine.rule(case.case_id, "arb-1", contract)

        assert engine.get_case(case.case_id) is not None
        assert engine.get_case(case.case_id).status == "ruled"
        assert engine.get_ruling(ruling.ruling_id) is not None
        assert engine.get_case_ruling(case.case_id) is not None

    def test_nonexistent_case(self, engine: ArbitrationEngine) -> None:
        assert engine.get_case("nonexistent") is None

        with pytest.raises(KeyError):
            engine.rule("nonexistent", "arb-1", ServiceContract(
                contract_id="x", parties=["a", "b"],
                terms=ContractTerms(price=0),
            ))
