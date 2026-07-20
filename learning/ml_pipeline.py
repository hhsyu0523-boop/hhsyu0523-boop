from __future__ import annotations

from typing import Any

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class SimpleMLPipeline:
    """Starter machine learning pipeline scaffold."""

    def __init__(self) -> None:
        self.pipeline = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("classifier", SVC(kernel="linear", probability=True)),
            ]
        )

    def fit(self, X: Any, y: Any) -> "SimpleMLPipeline":
        self.pipeline.fit(X, y)
        return self

    def predict(self, X: Any) -> Any:
        return self.pipeline.predict(X)
