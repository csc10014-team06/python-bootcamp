from datetime import date
import pytest

from shared.contract import Task
from shared.study_planner.validate import validate


def test_validate_valid_tasks():
    today = date(2026, 10, 26)
    tasks = [
        Task(title="Assignment", importance=4, effort_h=2.0, deadline=date(2026, 10, 27)),
        Task(title="DS Exam", importance=5, effort_h=6.0, deadline=date(2026, 10, 30)),
    ]
    # Dữ liệu chuẩn phải trả về mảng rỗng (không có lỗi)
    assert validate(tasks, today) == []


def test_validate_empty_task_list():
    today = date(2026, 10, 26)
    errors = validate([], today)
    assert len(errors) == 1
    assert "empty" in errors[0].lower()


def test_validate_invalid_inputs():
    today = date(2026, 10, 26)
    tasks = [
        Task(title="", importance=3, effort_h=2.0, deadline=date(2026, 10, 28)),          # Title rỗng
        Task(title="Past Task", importance=2, effort_h=1.0, deadline=date(2026, 10, 20)),  # Quá hạn
        Task(title="Bad Effort", importance=4, effort_h=-3.5, deadline=date(2026, 10, 29)),# Effort âm
    ]
    errors = validate(tasks, today)
    assert len(errors) == 3
    error_text = " ".join(errors).lower()
    assert "title cannot be empty" in error_text
    assert "overdue" in error_text
    assert "effort hours must be greater than 0" in error_text


def test_validate_duplicate_titles():
    today = date(2026, 10, 26)
    tasks = [
        Task(title="Review Git", importance=3, effort_h=1.0, deadline=date(2026, 10, 28)),
        Task(title="Review Git", importance=2, effort_h=2.0, deadline=date(2026, 10, 29)),
    ]
    errors = validate(tasks, today)
    assert len(errors) == 1
    assert "duplicate" in errors[0].lower()