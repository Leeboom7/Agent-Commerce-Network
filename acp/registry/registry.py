"""
ACP Service Registry.

The central directory where agents register their services and
discover services offered by other agents. The registry is the
"yellow pages" of the Agent Commerce Network.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass
class SearchResult:
    """A ranked search result from the registry."""

    listing: Any  # ServiceListing (avoid circular import)
    relevance_score: float
    match_reason: str = ""


class ServiceRegistry:
    """
    In-memory service registry for the Agent Commerce Network.

    Agents register ServiceListings. Other agents search and discover
    services by type, capability, or keyword.

    Thread-safe for single-process usage. In production, this would be
    backed by a search engine (Elasticsearch/Meilisearch).
    """

    def __init__(self) -> None:
        # listing_id -> ServiceListing
        self._listings: dict[str, Any] = {}
        # agent_id -> set of listing_ids
        self._by_agent: dict[str, set[str]] = defaultdict(set)
        # service_type -> set of listing_ids
        self._by_type: dict[str, set[str]] = defaultdict(set)
        # relationship_type -> set of listing_ids
        self._by_relationship: dict[str, set[str]] = defaultdict(set)
        # tag -> set of listing_ids
        self._by_tag: dict[str, set[str]] = defaultdict(set)

    # ── Registration ──────────────────────────────────────

    def register(self, listing: Any) -> str:
        """
        Register a service listing.

        Returns the listing_id.
        """
        lid = listing.listing_id
        self._listings[lid] = listing

        # Build indexes
        self._by_agent[listing.agent_id].add(lid)
        self._by_type[listing.service_type].add(lid)
        if listing.economic_relationship:
            self._by_relationship[listing.economic_relationship].add(lid)
        for tag in listing.tags:
            self._by_tag[tag.lower()].add(lid)

        listing.updated_at = datetime.now(UTC)
        return lid

    def unregister(self, listing_id: str) -> bool:
        """Remove a service listing. Returns True if it existed."""
        listing = self._listings.pop(listing_id, None)
        if listing is None:
            return False

        self._by_agent[listing.agent_id].discard(listing_id)
        self._by_type[listing.service_type].discard(listing_id)
        if listing.economic_relationship:
            self._by_relationship[listing.economic_relationship].discard(listing_id)
        for tag in listing.tags:
            self._by_tag[tag.lower()].discard(listing_id)

        return True

    def unregister_agent(self, agent_id: str) -> int:
        """Remove all listings for an agent. Returns count removed."""
        listing_ids = list(self._by_agent.get(agent_id, set()))
        for lid in listing_ids:
            self.unregister(lid)
        return len(listing_ids)

    # ── Lookup ────────────────────────────────────────────

    def get(self, listing_id: str) -> Any | None:
        """Get a listing by ID."""
        return self._listings.get(listing_id)

    def get_by_agent(self, agent_id: str) -> list[Any]:
        """Get all listings for an agent."""
        ids = self._by_agent.get(agent_id, set())
        return [self._listings[lid] for lid in ids if lid in self._listings]

    # ── Search & Discovery ────────────────────────────────

    def search(
        self,
        query: str = "",
        service_type: str | None = None,
        relationship_type: str | None = None,
        min_reputation: float = 0.0,
        required_capabilities: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        limit: int = 20,
    ) -> list[SearchResult]:
        """
        Search for services matching the given criteria.

        Results are ranked by:
        1. Reputation score (higher is better)
        2. Transaction volume (higher is better)
        3. Keyword relevance
        """
        candidates: set[str] = set()

        # Filter by type
        if service_type:
            candidates = self._by_type.get(service_type, set()).copy()
        elif relationship_type:
            candidates = self._by_relationship.get(relationship_type, set()).copy()
        else:
            candidates = set(self._listings.keys())

        if not candidates:
            return []

        results: list[SearchResult] = []

        for lid in candidates:
            listing = self._listings.get(lid)
            if listing is None:
                continue

            # Filter by minimum reputation
            if listing.reputation_score < min_reputation:
                continue

            # Filter by capabilities
            if required_capabilities and not listing.matches_capability(required_capabilities):
                continue

            # Filter by tags
            if tags:
                listing_tags = {t.lower() for t in listing.tags}
                if not listing_tags.intersection(t.lower() for t in tags):
                    continue

            # Calculate relevance
            relevance = listing.reputation_score / 100.0

            if query:
                keyword_score = self._keyword_relevance(listing, query)
                if keyword_score == 0:
                    continue
                relevance *= keyword_score

            results.append(SearchResult(
                listing=listing,
                relevance_score=round(relevance, 3),
                match_reason=self._build_match_reason(listing, query, service_type),
            ))

        # Rank by relevance, then by reputation, then by volume
        results.sort(
            key=lambda r: (
                r.relevance_score,
                r.listing.reputation_score,
                r.listing.total_transactions,
            ),
            reverse=True,
        )

        return results[:limit]

    def discover(
        self,
        relationship_type: str,
        min_reputation: float = 50.0,
        limit: int = 10,
    ) -> list[SearchResult]:
        """
        Discover agents capable of a specific economic relationship type.
        Shortcut for the most common discovery pattern.
        """
        return self.search(
            relationship_type=relationship_type,
            min_reputation=min_reputation,
            limit=limit,
        )

    # ── Helpers ───────────────────────────────────────────

    def _keyword_relevance(self, listing: Any, query: str) -> float:
        """Calculate keyword relevance score."""
        if listing.matches_query(query):
            return 1.0
        return 0.0

    def _build_match_reason(
        self, listing: Any, query: str, service_type: str | None
    ) -> str:
        parts = []
        if service_type:
            parts.append(f"Matches type: {service_type}")
        if query and listing.matches_query(query):
            parts.append(f"Matches query: {query}")
        return "; ".join(parts) if parts else "Reputation-based match"

    # ── Stats ─────────────────────────────────────────────

    @property
    def total_listings(self) -> int:
        return len(self._listings)

    @property
    def total_agents(self) -> int:
        return len(self._by_agent)

    def get_stats(self) -> dict[str, Any]:
        """Get registry statistics."""
        type_counts = {t: len(ids) for t, ids in self._by_type.items()}
        rel_counts = {r: len(ids) for r, ids in self._by_relationship.items()}
        return {
            "total_listings": self.total_listings,
            "total_agents": self.total_agents,
            "by_service_type": type_counts,
            "by_relationship_type": rel_counts,
        }
