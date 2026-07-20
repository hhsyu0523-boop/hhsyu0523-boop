from __future__ import annotations

from typing import Any

import pandas as pd


class FeaturePipeline:
    """Automatic feature generation for lottery datasets."""

    def generate(self, frame: pd.DataFrame) -> pd.DataFrame:
        if frame.empty:
            return frame

        features = frame.copy()
        features["number_count"] = features["numbers"].apply(lambda values: len(values) if isinstance(values, list) else 0)
        features["sum_numbers"] = features["numbers"].apply(lambda values: sum(values) if isinstance(values, list) else 0)
        features["min_number"] = features["numbers"].apply(lambda values: min(values) if isinstance(values, list) else 0)
        features["max_number"] = features["numbers"].apply(lambda values: max(values) if isinstance(values, list) else 0)
        features["mean_number"] = features["numbers"].apply(lambda values: (sum(values) / len(values)) if isinstance(values, list) and values else 0)
        features["repeat_flag"] = features["numbers"].apply(lambda values: 1 if len(values) != len(set(values)) else 0)
        return features
