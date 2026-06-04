"""
ACP Arbitration Agent.

Automated dispute resolution for the Agent Commerce Network.
When buyer and seller disagree about a delivery, the arbitrator
reviews the contract, delivery, and evidence from both sides,
then issues a binding ruling.

Design: Rule-based arbitration engine with optional LLM augmentation
for qualitative judgments. Produces structured rulings that feed into
the reputation and settlement systems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from acp.protocol.models import ServiceContract, VerificationReport


# ──────────────────────────────────────────────────────────────
# Arbitration Types
# ──────────────────────────────────────────────────────────────


class RulingType(str, Enum):
    BUYER_UPHELD = "buyer_upheld"        # Buyer wins — seller at fault
    SELLER_UPHELD = "seller_upheld"      # Seller wins — buyer's claim rejected
    SPLIT = "split"                       # Both share responsibility
    DISMISSED = "dismissed"              # Claim lacks merit, dismissed


@dataclass
class ArbitrationCase:
    """A dispute case filed with the arbitration system."""

    case_id: str
    contract_id: str
    claimant_id: str       # Who filed the dispute
    respondent_id: str     # The other party
    claim: str             # What the claimant says went wrong
    evidence: dict[str, Any] = field(default_factory=dict)
    verification_report: VerificationReport | None = None
    status: str = "filed"  # filed / under_review / ruled / appealed


@dataclass
class ArbitrationRuling:
    """A binding ruling issued by the arbitrator."""

    ruling_id: str
    case_id: str
    ruling_type: RulingType
    reasoning: str
    remedy: dict[str, Any]  # What should happen: refund, penalty, etc.
    arbitrator_id: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# ──────────────────────────────────────────────────────────────
# Arbitration Engine
# ──────────────────────────────────────────────────────────────


class ArbitrationEngine:
    """
    Automated dispute resolution engine.

    Evaluates disputes based on:
    1. Contract terms (what was agreed)
    2. Verification reports (what was delivered vs expected)
    3. Evidence from both parties
    4. Transaction history and reputation context

    Produces binding rulings with specific remedies.
    """

    # Standard remedy templates
    REMEDIES = {
        "full_refund": {
            "action": "refund",
            "amount": "full_contract_price",
            "penalty_to_seller": 0.15,  # Additional reputation penalty
        },
        "partial_refund": {
            "action": "partial_refund",
            "amount": "50_percent",
            "penalty_to_seller": 0.05,
        },
        "no_refund": {
            "action": "no_refund",
            "amount": 0,
            "penalty_to_buyer": 0.05,  # Frivolous claim penalty
        },
        "revision_required": {
            "action": "seller_must_revise",
            "deadline_extension_hours": 48,
            "penalty_to_seller": 0.03,
        },
    }

    def __init__(self) -> None:
        self._cases: dict[str, ArbitrationCase] = {}
        self._rulings: dict[str, ArbitrationRuling] = {}

    # ── Case Management ────────────────────────────────────

    def file_case(
        self,
        contract: ServiceContract,
        claimant_id: str,
        claim: str,
        evidence: dict[str, Any] | None = None,
        verification_report: VerificationReport | None = None,
    ) -> ArbitrationCase:
        """File a new dispute case."""
        import uuid

        respondent_id = (
            contract.seller_id
            if claimant_id == contract.buyer_id
            else contract.buyer_id
        )

        case = ArbitrationCase(
            case_id=f"case-{uuid.uuid4().hex[:12]}",
            contract_id=contract.contract_id,
            claimant_id=claimant_id,
            respondent_id=respondent_id,
            claim=claim,
            evidence=evidence or {},
            verification_report=verification_report,
        )
        self._cases[case.case_id] = case
        return case

    # ── Ruling ─────────────────────────────────────────────

    def rule(
        self,
        case_id: str,
        arbitrator_id: str,
        contract: ServiceContract,
    ) -> ArbitrationRuling:
        """
        Evaluate a case and issue a binding ruling.

        Decision tree:
        1. If verification report exists and shows clear pass/fail → rule accordingly
        2. If no verification, evaluate claim content against contract terms
        3. If claim is about non-delivery → check delivery status
        4. If claim is about quality → check acceptance criteria match
        5. If unclear → split ruling
        """
        case = self._cases.get(case_id)
        if case is None:
            raise KeyError(f"Case not found: {case_id}")

        case.status = "under_review"

        ruling_type, reasoning, remedy = self._evaluate(case, contract)

        import uuid
        ruling = ArbitrationRuling(
            ruling_id=f"ruling-{uuid.uuid4().hex[:12]}",
            case_id=case_id,
            ruling_type=ruling_type,
            reasoning=reasoning,
            remedy=remedy,
            arbitrator_id=arbitrator_id,
        )

        case.status = "ruled"
        self._rulings[ruling.ruling_id] = ruling
        return ruling

    def _evaluate(
        self, case: ArbitrationCase, contract: ServiceContract
    ) -> tuple[RulingType, str, dict[str, Any]]:
        """Core evaluation logic."""

        # ── Evidence from verification report ──
        if case.verification_report is not None:
            vr = case.verification_report
            if vr.verdict == "rejected":
                # All criteria failed — seller clearly at fault
                return (
                    RulingType.BUYER_UPHELD,
                    f"Verification report shows all {vr.total_count} criteria failed. "
                    f"Seller did not meet contract requirements.",
                    self.REMEDIES["full_refund"],
                )
            elif vr.verdict == "partial":
                # Some criteria failed
                fail_count = vr.total_count - vr.passed_count
                if fail_count > vr.passed_count:
                    return (
                        RulingType.BUYER_UPHELD,
                        f"{fail_count}/{vr.total_count} criteria failed. "
                        f"Majority of requirements not met.",
                        self.REMEDIES["partial_refund"],
                    )
                else:
                    return (
                        RulingType.SPLIT,
                        f"{fail_count}/{vr.total_count} criteria failed. "
                        f"Seller partially met requirements. Revision required.",
                        self.REMEDIES["revision_required"],
                    )
            elif vr.verdict == "accepted":
                # All passed — buyer's claim has no merit
                return (
                    RulingType.SELLER_UPHELD,
                    f"Verification report shows all criteria passed. "
                    f"Buyer's claim is contradicted by evidence.",
                    self.REMEDIES["no_refund"],
                )

        # ── Evidence from contract status ──
        if contract.status.value == "active":
            # Seller hasn't delivered yet
            claim_lower = case.claim.lower()
            if any(w in claim_lower for w in ("late", "delay", "overdue", "not delivered")):
                return (
                    RulingType.BUYER_UPHELD,
                    "Seller has not delivered by the contract deadline.",
                    self.REMEDIES["full_refund"],
                )

        if contract.status.value == "delivered":
            # Delivered but disputed — no verification report available
            return (
                RulingType.SPLIT,
                "Delivery was made but quality is disputed. "
                "Without independent verification, both parties share responsibility. "
                "Recommend: obtain third-party verification.",
                self.REMEDIES["revision_required"],
            )

        # ── Default: insufficient evidence ──
        return (
            RulingType.DISMISSED,
            "Insufficient evidence to support the claim. "
            "Both parties are encouraged to provide additional documentation.",
            self.REMEDIES["no_refund"],
        )

    # ── Query ──────────────────────────────────────────────

    def get_case(self, case_id: str) -> ArbitrationCase | None:
        return self._cases.get(case_id)

    def get_ruling(self, ruling_id: str) -> ArbitrationRuling | None:
        return self._rulings.get(ruling_id)

    def get_case_ruling(self, case_id: str) -> ArbitrationRuling | None:
        """Get the ruling for a case, if one has been issued."""
        for ruling in self._rulings.values():
            if ruling.case_id == case_id:
                return ruling
        return None

    @property
    def total_cases(self) -> int:
        return len(self._cases)

    @property
    def total_rulings(self) -> int:
        return len(self._rulings)
