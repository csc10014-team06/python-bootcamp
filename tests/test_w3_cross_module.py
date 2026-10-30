"""Isolated unit tests for the shared study planner modules (T-W3)."""

from datetime import date

import pytest

from shared.contract import Block, Task
from shared.study_planner.allocate import allocate
from shared.study_planner.leftover import unscheduled
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render
from shared.study_planner.validate import validate


def test_parse_csv_reads_tasks(tmp_path):
    path = tmp_path / "tasks.csv"
    path.write_text(
        "title,importance,effort_h,deadline\n"
        "Python,5,2.5,2026-11-02\n"
        "Math,3,1.0,2026-11-05\n",
        encoding="utf-8",
    )

    tasks = parse_csv(path)

    assert len(tasks) == 2
    assert isinstance(tasks[0], Task)
    assert tasks[0].title == "Python"
    assert tasks[0].effort_h == 2.5
    assert tasks[1].deadline == date(2026, 11, 5)


def test_parse_csv_rejects_missing_column(tmp_path):
    path = tmp_path / "tasks.csv"
    path.write_text("title,importance,effort_h\nPython,5,2.5\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing column"):
        parse_csv(path)


def test_validate_accepts_valid_tasks():
    today = date(2026, 10, 30)
    tasks = [Task("Python", 5, 2.0, date(2026, 11, 2))]

    assert validate(tasks, today) == []


def test_validate_reports_invalid_fields():
    today = date(2026, 10, 30)
    tasks = [Task("   ", 0, -1.0, date(2026, 10, 29))]

    errors = validate(tasks, today)

    assert len(errors) == 4
    assert any("Title cannot be empty" in e for e in errors)
    assert any("Importance must be between 1 and 5" in e for e in errors)
    assert any("Effort hours must be greater than 0" in e for e in errors)
    assert any("already overdue" in e for e in errors)


def test_prioritise_orders_tasks_without_mutating_input():
    today = date(2026, 10, 30)
    later = Task("Later", 5, 3.0, date(2026, 11, 9))
    urgent = Task("Urgent", 3, 1.0, date(2026, 10, 31))
    due_today = Task("Due today", 4, 1.0, today)
    tasks = [later, urgent, due_today]

    ordered = prioritise(tasks, today)

    assert ordered == [due_today, urgent, later]
    assert tasks == [later, urgent, due_today]


def test_allocate_splits_hours_and_preserves_task_identity():
    first = Task("Python", 5, 2.0, date(2026, 11, 2))
    second = Task("Math", 3, 3.0, date(2026, 11, 5))

    blocks = allocate([first, second], hours=3.0)

    assert len(blocks) == 2
    assert blocks[0].task is first
    assert blocks[0].hours == pytest.approx(2.0)
    assert blocks[1].task is second
    assert blocks[1].hours == pytest.approx(1.0)


def test_allocate_rejects_negative_hours():
    with pytest.raises(ValueError, match="negative"):
        allocate([], hours=-1)


def test_render_describes_partial_block_and_total():
    task = Task("Python", 5, 3.0, date(2026, 11, 2))

    output = render([Block(task=task, hours=1.0)])

    assert "Python" in output
    assert "1 of 3 h" in output
    assert "Total: 1 h" in output


def test_render_empty_plan():
    assert render([]) == "No study blocks planned."


def test_unscheduled_keeps_only_remaining_hours():
    first = Task("Python", 5, 2.0, date(2026, 11, 2))
    second = Task("Math", 3, 3.0, date(2026, 11, 5))
    blocks = [Block(task=first, hours=2.0), Block(task=second, hours=1.0)]

    leftovers = unscheduled([first, second], blocks)

    assert len(leftovers) == 1
    assert leftovers[0].title == "Math"
    assert leftovers[0].effort_h == pytest.approx(2.0)
    assert second.effort_h == 3.0  # Original Task must remain unchanged.
