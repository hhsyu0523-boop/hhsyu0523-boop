from __future__ import annotations

from typing import Any


class RollingBacktest:
    """Simple rolling backtest scaffold."""

    def __init__(self, window_size: int = 20) -> None:
        self.window_size = window_size

    def run(self, history: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "window_size": self.window_size,
            "history_length": len(history),
            "status": "ready",
            "summary": "Backtest scaffold initialized",
        }
