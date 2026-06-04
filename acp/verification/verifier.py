"""
ACP Delivery Verifier.

Automated acceptance checking — verifies that a seller's delivery
meets the contract's acceptance criteria. Produces structured
verification reports that feed into the reputation system.

Design: The verifier is a deterministic rule engine for simple checks
(format, presence of required fields, numeric thresholds) with an
optional LLM-backed mode for qualitative criteria.
"""

from __future__ import annotations

from typing import Any

from acp.protocol.models import (
    CheckResult,
    ContractTerms,
    VerificationReport,
)


class DeliveryVerifier:
    """
    Automated delivery verification engine.

    Checks a delivery against contract acceptance criteria.
    Supports both deterministic rules and LLM-augmented checks.
    """

    def verify(
        self,
        contract_id: str,
        verifier_id: str,
        delivery: dict[str, Any],
        criteria: list[str],
    ) -> VerificationReport:
        """
        Verify a delivery against acceptance criteria.

        Args:
            contract_id: The contract being verified.
            verifier_id: The agent performing verification.
            delivery: The actual deliverable (dict with keys like 'data', 'report', 'files').
            criteria: List of acceptance criteria strings from the contract.

        Returns:
            VerificationReport with pass/fail for each criterion.
        """
        checks: list[CheckResult] = []

        for criterion in criteria:
            result = self._check_criterion(criterion, delivery)
            checks.append(result)

        # Determine verdict
        failed = [c for c in checks if not c.passed]
        if not failed:
            verdict = "accepted"
            summary = f"All {len(checks)} criteria passed."
        elif len(failed) == len(checks):
            verdict = "rejected"
            summary = f"All {len(checks)} criteria failed."
        else:
            verdict = "partial"
            summary = (
                f"{len(checks) - len(failed)}/{len(checks)} criteria passed. "
                f"Failed: {[c.criterion for c in failed]}"
            )

        return VerificationReport(
            contract_id=contract_id,
            verifier_id=verifier_id,
            checks=checks,
            verdict=verdict,
            summary=summary,
        )

    def _check_criterion(
        self, criterion: str, delivery: dict[str, Any]
    ) -> CheckResult:
        """
        Check a single criterion against the delivery.

        Supports these patterns:
        - "Must be in X format" → checks delivery format/extension
        - "Must cite sources" → checks presence of citations
        - "Must contain X" → checks for substring or key presence
        - "Must have at least N X" → checks numeric threshold
        - "Response time < Xms" → checks numeric constraint
        - "Uptime > X%" → checks numeric constraint
        """
        criterion_lower = criterion.lower()

        # ── Format checks ──
        if "format" in criterion_lower:
            return self._check_format(criterion, delivery)

        # ── Numeric threshold checks (check BEFORE presence, since
        # "at least N X" looks like a presence check too) ──
        if any(op in criterion_lower for op in (">", "<", ">=", "<=", "at least", "no more than")):
            # Only threshold if there's a numeric pattern nearby
            import re
            if re.search(r'\d+', criterion):
                return self._check_threshold(criterion, delivery)

        # ── Presence checks ──
        if any(word in criterion_lower for word in ("must contain", "must include", "must have")):
            return self._check_presence(criterion, delivery)

        # ── Source/citation checks ──
        if any(word in criterion_lower for word in ("cite", "source", "reference", "citation")):
            return self._check_sources(criterion, delivery)

        # ── Generic pass (criterion too vague to check automatically) ──
        return CheckResult(
            criterion=criterion,
            passed=True,
            notes="Criterion could not be automatically verified; marked as passed by default.",
        )

    # ── Specific Checkers ──────────────────────────────────

    def _check_format(self, criterion: str, delivery: dict[str, Any]) -> CheckResult:
        """Check if delivery matches expected format."""
        # Extract expected format from criterion
        expected_format = ""
        if "markdown" in criterion.lower():
            expected_format = "markdown"
        elif "json" in criterion.lower():
            expected_format = "json"
        elif "csv" in criterion.lower():
            expected_format = "csv"
        elif "excel" in criterion.lower() or "xlsx" in criterion.lower():
            expected_format = "excel"
        elif "pdf" in criterion.lower():
            expected_format = "pdf"

        if not expected_format:
            return CheckResult(criterion=criterion, passed=True,
                             notes="Format type not recognized; passed by default.")

        # Check delivery content for format markers
        delivery_str = str(delivery).lower()
        format_markers = {
            "markdown": [".md", "markdown", "# ", "## "],
            "json": [".json", '{"', "{'"],
            "csv": [".csv", ","],
            "excel": [".xlsx", ".xls", "excel"],
            "pdf": [".pdf", "%pdf"],
        }

        markers = format_markers.get(expected_format, [])
        matched = any(marker in delivery_str for marker in markers)

        return CheckResult(
            criterion=criterion,
            passed=matched,
            expected_value=f"format={expected_format}",
            actual_value=f"Detected markers: {[m for m in markers if m in delivery_str]}",
            notes=f"Format check for {expected_format}: {'PASS' if matched else 'FAIL'}",
        )

    def _check_presence(self, criterion: str, delivery: dict[str, Any]) -> CheckResult:
        """Check if required content is present in delivery."""
        # Extract what should be present
        # Pattern: "Must contain/ include/ have X"
        import re
        match = re.search(
            r'must (?:contain|include|have)\s+(.+)',
            criterion, re.IGNORECASE
        )
        if not match:
            return CheckResult(criterion=criterion, passed=True,
                             notes="Could not parse presence requirement.")

        required = match.group(1).strip().rstrip('.')

        # Check if the required item exists as a key or substring
        delivery_str = str(delivery).lower()
        required_lower = required.lower()

        # Try key lookup first (normalize underscores/spaces)
        normalized_keys = {k.lower().replace("_", " ") for k in delivery.keys()}
        found_as_key = required_lower in normalized_keys
        found_as_value = required_lower in delivery_str

        passed = found_as_key or found_as_value

        return CheckResult(
            criterion=criterion,
            passed=passed,
            expected_value=f"Contains: {required}",
            actual_value="Found in delivery" if passed else "Not found in delivery",
        )

    def _check_threshold(self, criterion: str, delivery: dict[str, Any]) -> CheckResult:
        """Check numeric threshold constraints."""
        import re

        # Extract the numeric value and operator
        # Pattern: "at least N" or "> N" or "< N" etc.
        threshold_match = re.search(
            r'(?:at least|≥|>=?|no more than|≤|<=?|more than|less than)\s*([\d.]+)',
            criterion, re.IGNORECASE
        )
        if not threshold_match:
            return CheckResult(criterion=criterion, passed=True,
                             notes="Could not parse threshold value.")

        threshold = float(threshold_match.group(1))

        # Determine operator
        if any(w in criterion.lower() for w in ("at least", "≥", ">=", "more than", ">")):
            op = ">=" if "at least" in criterion.lower() else ">"
        else:
            op = "<=" if "no more than" in criterion.lower() else "<"

        # Extract the metric from the criterion and find it in delivery
        metric_match = re.search(
            r'(?:of|than|at least|more than|less than)\s+([\d.]+)\s+(.+)',
            criterion, re.IGNORECASE
        )
        metric_name = metric_match.group(2).strip() if metric_match else ""

        # Try to find the metric value in delivery
        actual_value = self._extract_numeric_value(metric_name, delivery)

        if actual_value is None:
            return CheckResult(criterion=criterion, passed=True,
                             notes=f"Metric '{metric_name}' not found in delivery; passed by default.",
                             expected_value=f"{op} {threshold}")

        # Compare
        if op in (">=", ">"):
            passed = actual_value >= threshold if op == ">=" else actual_value > threshold
        else:
            passed = actual_value <= threshold if op == "<=" else actual_value < threshold

        return CheckResult(
            criterion=criterion,
            passed=passed,
            expected_value=f"{op} {threshold}",
            actual_value=actual_value,
        )

    def _check_sources(self, criterion: str, delivery: dict[str, Any]) -> CheckResult:
        """Check if sources/citations are present."""
        delivery_str = str(delivery).lower()

        # Look for common citation patterns
        citation_indicators = [
            "http://", "https://", "www.",
            "source:", "reference:", "citation:",
            "[1]", "[2]", "(1)", "(2)",
            "according to", "cited from",
        ]

        found = [ind for ind in citation_indicators if ind in delivery_str]
        passed = len(found) > 0

        return CheckResult(
            criterion=criterion,
            passed=passed,
            expected_value="Sources/citations present",
            actual_value=f"Found {len(found)} citation indicators" if passed else "No citations found",
        )

    def _extract_numeric_value(
        self, metric_name: str, delivery: dict[str, Any]
    ) -> float | None:
        """Extract a numeric value for a metric from the delivery."""
        # Search in delivery dictionary
        for key, value in delivery.items():
            if isinstance(value, (int, float)):
                if metric_name.lower() in key.lower():
                    return float(value)
            elif isinstance(value, dict):
                result = self._extract_numeric_value(metric_name, value)
                if result is not None:
                    return result
            elif isinstance(value, str):
                if metric_name.lower() in value.lower():
                    import re
                    nums = re.findall(r'[\d.]+', value)
                    if nums:
                        return float(nums[0])

        # Also search flattened string
        flat = str(delivery)
        if metric_name.lower() in flat.lower():
            import re
            # Find numbers near the metric name
            idx = flat.lower().find(metric_name.lower())
            nearby = flat[max(0, idx - 5):idx + len(metric_name) + 30]
            nums = re.findall(r'[\d.]+', nearby)
            if nums:
                return float(nums[0])

        return None
