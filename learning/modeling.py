from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class LotteryModelTrainer:
    """Trains a simple machine learning model from engineered features."""

    def __init__(self) -> None:
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)

    def train(self, features: pd.DataFrame) -> dict[str, Any]:
        if features.empty:
            return {"status": "no_data", "accuracy": 0.0}

        target = features["sum_numbers"].astype(int)
        X = features[["number_count", "sum_numbers", "min_number", "max_number", "mean_number", "repeat_flag"]]
        y = (target > target.median()).astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        return {"status": "trained", "accuracy": float(accuracy)}
