from __future__ import annotations

from typing import Any


class EvaluationReporter:
    """Generates simple evaluation summaries for prediction runs."""

    def generate(self, results: dict[str, Any]) -> dict[str, Any]:
        return {
            "summary": "Evaluation scaffold ready",
            "engines": sorted(results.keys()),
            "count": len(results),
        }
