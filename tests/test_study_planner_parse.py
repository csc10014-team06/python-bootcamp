from datetime import date
from pathlib import Path

import pytest

from shared.contract import Task
from shared.study_planner.parse import parse_csv

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_parse_sample():
    assert parse_csv(SAMPLES / "tasks.csv") == [
        Task("DS exam", 5, 6.0, date(2026, 10, 30)),
        Task("Assignment", 4, 1.5, date(2026, 10, 27)),
    ]


def test_bad_value_reports_line():
    with pytest.raises(ValueError, match="line 3"):
        parse_csv(SAMPLES / "tasks_bad.csv")


def test_empty_value(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("title,importance,effort_h,deadline\n,3,1,2026-10-27\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Empty value on line 2"):
        parse_csv(p)


def test_missing_column(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("title,importance,effort_h\nX,3,1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="deadline"):
        parse_csv(p)


def test_strips_whitespace_and_header_only(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("title,importance,effort_h,deadline\n Read , 2 , 0.5 , 2026-11-01 \n", encoding="utf-8")
    assert parse_csv(p) == [Task("Read", 2, 0.5, date(2026, 11, 1))]
    p.write_text("title,importance,effort_h,deadline\n", encoding="utf-8")
    assert parse_csv(p) == []


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_csv("does_not_exist.csv")
