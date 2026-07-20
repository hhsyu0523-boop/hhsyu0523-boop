from __future__ import annotations

from typing import Any

import pandas as pd


class FeatureEngineer:
    """Simple feature engineering scaffold for future model development."""

    def __init__(self) -> None:
        self.feature_names: list[str] = ["lag_1", "lag_2", "frequency_score"]

    def build_features(self, data: pd.DataFrame) -> pd.DataFrame:
        frame = data.copy()
        if frame.empty:
            return frame
        frame["lag_1"] = frame.iloc[:, 0].shift(1).fillna(0)
        frame["lag_2"] = frame.iloc[:, 0].shift(2).fillna(0)
        frame["frequency_score"] = frame.iloc[:, 0].astype(int).rank(method="first")
        return frame
