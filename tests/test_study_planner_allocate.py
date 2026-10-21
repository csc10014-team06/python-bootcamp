"""Unit tests for shared.study_planner.allocate."""

from datetime import date

import pytest

from shared.contract import Block, Task
from shared.study_planner.allocate import allocate


def test_allocate_partial_budget():
    """Test when total effort exceeds available hours; last task is partially allocated."""
    t1 = Task("Assignment", 4, 1.5, date(2026, 10, 27))
    t2 = Task("DS exam", 5, 6.0, date(2026, 10, 30))
    blocks = allocate([t1, t2], 2.0)

    assert len(blocks) == 2
    assert blocks[0] == Block(task=t1, hours=1.5)
    assert blocks[1] == Block(task=t2, hours=0.5)


def test_allocate_all_tasks_fit():
    """Test when available hours exceed total effort; all tasks are fully scheduled."""
    t1 = Task("Task A", 3, 1.0, date(2026, 10, 28))
    t2 = Task("Task B", 2, 2.0, date(2026, 10, 29))
    blocks = allocate([t1, t2], 5.0)

    assert len(blocks) == 2
    assert blocks[0] == Block(task=t1, hours=1.0)
    assert blocks[1] == Block(task=t2, hours=2.0)


def test_allocate_exact_fit():
    """Test when available hours exactly equal total effort."""
    t1 = Task("Task A", 4, 2.5, date(2026, 10, 28))
    t2 = Task("Task B", 3, 1.5, date(2026, 10, 29))
    blocks = allocate([t1, t2], 4.0)

    assert len(blocks) == 2
    assert blocks[0] == Block(task=t1, hours=2.5)
    assert blocks[1] == Block(task=t2, hours=1.5)


def test_allocate_budget_runs_out_on_first_task():
    """Test when first task already requires more than the available hours."""
    t1 = Task("Big Task", 5, 5.0, date(2026, 10, 28))
    t2 = Task("Small Task", 3, 1.0, date(2026, 10, 29))
    blocks = allocate([t1, t2], 3.0)

    assert len(blocks) == 1
    assert blocks[0] == Block(task=t1, hours=3.0)


def test_allocate_zero_hours():
    """Test that zero available hours returns an empty list."""
    t1 = Task("Task A", 3, 2.0, date(2026, 10, 28))
    assert allocate([t1], 0.0) == []


def test_allocate_empty_tasks():
    """Test allocating with an empty list of tasks."""
    assert allocate([], 5.0) == []


def test_allocate_negative_hours_raises():
    """Test that negative available hours raises ValueError."""
    t1 = Task("Task A", 3, 2.0, date(2026, 10, 28))
    with pytest.raises(ValueError, match="negative"):
        allocate([t1], -1.0)


def test_allocate_skips_zero_effort():
    """Test that tasks with 0 effort are skipped and do not produce blocks."""
    t1 = Task("Zero Effort Task", 1, 0.0, date(2026, 10, 28))
    t2 = Task("Real Task", 3, 2.0, date(2026, 10, 29))
    blocks = allocate([t1, t2], 2.0)

    assert len(blocks) == 1
    assert blocks[0] == Block(task=t2, hours=2.0)
