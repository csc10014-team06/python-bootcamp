"""Comprehensive unit tests for nhat_dm's Week 3 homework modules."""

from datetime import date
from pathlib import Path
import pytest

from members.nhat_dm.w3.dates import parse_due
from members.nhat_dm.w3.log_stats import analyse
from members.nhat_dm.w3.cli import main

BASE_DIR = Path(__file__).resolve().parents[3]
SAMPLE_CSV = BASE_DIR / "samples" / "tasks.csv"
TODAY = date(2026, 10, 6)  # Tuesday


def test_parse_due_standard() -> None:
    assert parse_due("2026-10-30", TODAY) == date(2026, 10, 30)
    assert parse_due("tomorrow", TODAY) == date(2026, 10, 7)
    assert parse_due("TOMORROW", TODAY) == date(2026, 10, 7)
    assert parse_due("today", TODAY) == date(2026, 10, 6)
    assert parse_due("in 3 days", TODAY) == date(2026, 10, 9)
    assert parse_due("in 1 day", TODAY) == date(2026, 10, 7)
    assert parse_due("Fri", TODAY) == date(2026, 10, 9)
    assert parse_due("Friday", TODAY) == date(2026, 10, 9)
    assert parse_due("Tue", TODAY) == date(2026, 10, 13)
    assert parse_due("Tuesday", TODAY) == date(2026, 10, 13)


def test_parse_due_invalid() -> None:
    for invalid in ["", "  ", "someday", "next week", "in days", "in ten days", "2026/10/30"]:
        with pytest.raises(ValueError):
            parse_due(invalid, TODAY)
    with pytest.raises(ValueError):
        parse_due(123, TODAY)  # type: ignore[arg-type]


def test_analyse_stats() -> None:
    pairs = [("fee", 100), ("fee", 300), ("rag", 900), ("rag", 1100), ("fee", 200)]
    res = analyse(pairs)
    assert res["counts"]["fee"] == 3
    assert res["counts"]["rag"] == 2
    assert res["p95"]["fee"] == 300
    assert res["p95"]["rag"] == 1100
    assert res["slowest"] == "rag"


def test_analyse_empty() -> None:
    res = analyse([])
    assert len(res["counts"]) == 0
    assert res["p95"] == {}
    assert res["slowest"] is None


def test_cli_success(capsys: pytest.CaptureFixture[str]) -> None:
    code = main([str(SAMPLE_CSV), "--hours", "2", "--today", "2026-10-26"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Tonight (2.0 h):" in captured.out
    assert "Assignment" in captured.out
    assert "DS exam" in captured.out


def test_cli_errors(capsys: pytest.CaptureFixture[str]) -> None:
    # Missing file
    code1 = main(["non_existent.csv", "--hours", "2"])
    assert code1 == 1

    # Negative hours
    code2 = main([str(SAMPLE_CSV), "--hours", "-1"])
    assert code2 == 1

    # Invalid today date
    code3 = main([str(SAMPLE_CSV), "--today", "invalid-date"])
    assert code3 == 1
