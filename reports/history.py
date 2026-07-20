from __future__ import annotations

from typing import Any


class PredictionHistoryReporter:
    """Starter report helper for prediction history."""

    def summarize(self, history: list[dict[str, Any]]) -> dict[str, Any]:
        return {"count": len(history), "status": "history_ready"}
