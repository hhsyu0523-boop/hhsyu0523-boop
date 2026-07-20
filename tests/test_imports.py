from engine.base import BasePredictionEngine
from engine.numbers3_engine import Numbers3PredictionEngine
from learning.feature_engineering import FeatureEngineer
from prediction.box_priority import BoxPriorityEngine
from prediction.straight_optimization import StraightOptimizationEngine


def test_imports() -> None:
    assert issubclass(Numbers3PredictionEngine, BasePredictionEngine)
    assert isinstance(FeatureEngineer(), FeatureEngineer)
    assert isinstance(BoxPriorityEngine().generate(), list)
    assert isinstance(StraightOptimizationEngine().generate(), list)
