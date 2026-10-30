"""Unit tests for error handling module in study_planner (T-W3 Member 3: M.Nhật)."""

from datetime import date
from pathlib import Path
import pytest

from shared.contract import Task
from shared.study_planner.errors import (
    EmptyCSVError,
    InfeasiblePlan,
    check_feasible,
    check_file,
    validate_input,
)


def test_infeasible_plan_str() -> None:
    exc = InfeasiblePlan(needed_h=7.5, available_h=2.0)
    assert exc.needed_h == 7.5
    assert exc.available_h == 2.0
    assert "needed 7.5 h" in str(exc)
    assert "2.0 h available" in str(exc)


def test_check_feasible_success() -> None:
    tasks = [
        Task("Math", 5, 1.5, date(2026, 10, 30)),
        Task("Physics", 4, 0.5, date(2026, 10, 31)),
    ]
    assert check_feasible(tasks, available_h=2.0) is True
    assert check_feasible(tasks, available_h=5.0) is True


def test_check_feasible_raises_infeasible() -> None:
    tasks = [
        Task("Math", 5, 2.5, date(2026, 10, 30)),
        Task("Physics", 4, 1.0, date(2026, 10, 31)),
    ]
    with pytest.raises(InfeasiblePlan) as exc_info:
        check_feasible(tasks, available_h=3.0)
    assert exc_info.value.needed_h == 3.5
    assert exc_info.value.available_h == 3.0


def test_check_feasible_negative_hours() -> None:
    tasks = [Task("Math", 5, 1.0, date(2026, 10, 30))]
    with pytest.raises(ValueError, match="negative"):
        check_feasible(tasks, available_h=-1.0)


def test_check_file_missing(tmp_path: Path) -> None:
    missing_file = tmp_path / "does_not_exist.csv"
    with pytest.raises(FileNotFoundError):
        check_file(missing_file)


def test_check_file_empty(tmp_path: Path) -> None:
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")
    with pytest.raises(EmptyCSVError):
        check_file(empty_file)


def test_check_file_header_only(tmp_path: Path) -> None:
    header_only = tmp_path / "header_only.csv"
    header_only.write_text("title,importance,effort_h,deadline\n", encoding="utf-8")
    with pytest.raises(EmptyCSVError):
        check_file(header_only)


def test_check_file_valid(tmp_path: Path) -> None:
    valid_file = tmp_path / "valid.csv"
    valid_file.write_text(
        "title,importance,effort_h,deadline\nTask 1,5,2.0,2026-10-30\n",
        encoding="utf-8",
    )
    res = check_file(valid_file)
    assert res == valid_file


def test_validate_input_missing_file() -> None:
    errs = validate_input("missing_path_123.csv", available_h=2.0)
    assert len(errs) > 0
    assert any("not found" in e.lower() for e in errs)


def test_validate_input_negative_hours(tmp_path: Path) -> None:
    valid_file = tmp_path / "valid.csv"
    valid_file.write_text(
        "title,importance,effort_h,deadline\nTask 1,5,2.0,2026-10-30\n",
        encoding="utf-8",
    )
    errs = validate_input(valid_file, available_h=-2.0)
    assert len(errs) == 1
    assert "negative" in errs[0].lower()
