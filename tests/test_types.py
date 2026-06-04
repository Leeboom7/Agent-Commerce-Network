"""Tests for protocol types — the 18 economic relationship types."""

from acp.protocol.types import (
    CORE_RELATIONSHIP_TYPES,
    TOTAL_RELATIONSHIP_TYPES,
    CollaborationType,
    DiscreteTransactionType,
    EconomicRelationshipCategory,
    IntermediaryType,
    OngoingRelationshipType,
    TrustGovernanceType,
    get_category,
    is_core,
    list_by_category,
)


class TestEconomicRelationshipTypes:
    """Verify the protocol type definitions are complete and consistent."""

    def test_total_count(self) -> None:
        """All 18 relationship types are defined."""
        discrete = len(DiscreteTransactionType)
        ongoing = len(OngoingRelationshipType)
        intermediary = len(IntermediaryType)
        collaboration = len(CollaborationType)
        trust = len(TrustGovernanceType)
        total = discrete + ongoing + intermediary + collaboration + trust
        assert total == TOTAL_RELATIONSHIP_TYPES, f"Expected 18, got {total}"
        assert total == 18

    def test_discrete_transactions_exist(self) -> None:
        assert DiscreteTransactionType.PURCHASE.value == "purchase"
        assert DiscreteTransactionType.COMMISSION.value == "commission"
        assert DiscreteTransactionType.CONTRACT.value == "contract"

    def test_ongoing_relationships_exist(self) -> None:
        assert OngoingRelationshipType.SUBSCRIPTION.value == "subscription"
        assert OngoingRelationshipType.RETAINER.value == "retainer"
        assert OngoingRelationshipType.FRANCHISE.value == "franchise"
        assert OngoingRelationshipType.MODEL_RENTAL.value == "model_rental"

    def test_intermediary_types_exist(self) -> None:
        assert IntermediaryType.REFERRAL.value == "referral"
        assert IntermediaryType.AGGREGATION.value == "aggregation"
        assert IntermediaryType.OPEN_BOUNTY.value == "open_bounty"

    def test_collaboration_types_exist(self) -> None:
        assert CollaborationType.TEAM_FORMATION.value == "team_formation"
        assert CollaborationType.JOINT_VENTURE.value == "joint_venture"
        assert CollaborationType.REVENUE_SHARING.value == "revenue_sharing"

    def test_trust_governance_types_exist(self) -> None:
        assert TrustGovernanceType.VERIFICATION.value == "verification"
        assert TrustGovernanceType.ARBITRATION.value == "arbitration"
        assert TrustGovernanceType.INSURANCE.value == "insurance"
        assert TrustGovernanceType.ESCROW.value == "escrow"
        assert TrustGovernanceType.CAPITAL_ALLOCATION.value == "capital_allocation"

    def test_core_set_is_eight(self) -> None:
        """8 CORE types for MVP implementation."""
        assert len(CORE_RELATIONSHIP_TYPES) == 8
        assert "purchase" in CORE_RELATIONSHIP_TYPES
        assert "arbitration" in CORE_RELATIONSHIP_TYPES

    def test_get_category(self) -> None:
        assert get_category("purchase") == EconomicRelationshipCategory.DISCRETE_TRANSACTION
        assert get_category("subscription") == EconomicRelationshipCategory.ONGOING_RELATIONSHIP
        assert get_category("referral") == EconomicRelationshipCategory.INTERMEDIARY
        assert get_category("team_formation") == EconomicRelationshipCategory.COLLABORATION
        assert get_category("arbitration") == EconomicRelationshipCategory.TRUST_GOVERNANCE

    def test_get_category_unknown_raises(self) -> None:
        try:
            get_category("nonexistent")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_is_core(self) -> None:
        assert is_core("purchase") is True
        assert is_core("franchise") is False

    def test_list_by_category(self) -> None:
        discrete = list_by_category(EconomicRelationshipCategory.DISCRETE_TRANSACTION)
        assert len(discrete) == 3
        assert "purchase" in discrete
        assert "commission" in discrete
        assert "contract" in discrete
