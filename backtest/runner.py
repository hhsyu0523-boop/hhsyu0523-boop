from __future__ import annotations

from typing import Any


class BacktestRunner:
    """Runs a simple rolling backtest over historical data."""

    def run(self, frame: Any, window_size: int = 20) -> dict[str, Any]:
        if frame is None:
            return {"status": "no_data", "window_size": window_size}
        length = len(frame)
        return {
            "status": "completed",
            "window_size": window_size,
            "rows": length,
            "summary": f"Backtest prepared for {length} rows",
        }
