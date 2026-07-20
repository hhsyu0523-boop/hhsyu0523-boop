from pathlib import Path

from prediction.box_priority import BoxPriorityEngine


def test_export_report_writes_csv(tmp_path: Path) -> None:
    history = [
        {"numbers": [1, 2, 3]},
        {"numbers": [4, 5, 6]},
        {"numbers": [1, 4, 7]},
    ]
    engine = BoxPriorityEngine()
    output = tmp_path / "report.csv"
    engine.export_report(history=history, digits=3, limit=3, output_path=str(output))

    assert output.exists()
    assert output.read_text(encoding="utf-8").startswith("rank_type")
