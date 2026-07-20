from prediction.box_priority import BoxPriorityEngine


def test_box_priority_engine_generates_ranked_candidates() -> None:
    history = [
        {"draw": 1, "numbers": [1, 2, 3]},
        {"draw": 2, "numbers": [4, 5, 6]},
        {"draw": 3, "numbers": [1, 4, 7]},
        {"draw": 4, "numbers": [2, 5, 8]},
    ]

    engine = BoxPriorityEngine()
    result = engine.generate(history, digits=3, limit=5)

    assert isinstance(result, list)
    assert result
    assert all("combination" in item for item in result)
    assert all("score" in item for item in result)
