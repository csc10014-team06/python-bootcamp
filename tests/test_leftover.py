from datetime import date

from shared.contract import Task, Block
from shared.study_planner.leftover import unscheduled


def test_partial_allocation():
    task = Task("DS exam", 5, 6.0, date(2026, 10, 30))
    blocks = [Block(task, 2.0)]

    result = unscheduled([task], blocks)

    assert len(result) == 1
    assert result[0].effort_h == 4.0
    assert task.effort_h == 6.0

def test_multiple_blocks_same_task():
    task = Task("DS exam", 5, 6.0, date(2026, 10, 30))
    blocks = [Block(task, 2.0), Block(task, 1.5)]

    result = unscheduled([task], blocks)

    assert len(result) == 1
    assert result[0].effort_h == 2.5
    assert task.effort_h == 6.0

def test_fully_allocated_task():
    task = Task("DS exam", 5, 6.0, date(2026, 10, 30))
    blocks = [Block(task, 2.0), Block(task, 5.0)]

    result = unscheduled([task], blocks)

    assert len(result) == 0
    assert task.effort_h == 6.0

def test_no_blocks():
    tasks = [
            Task("DS exam", 5, 6.0, date(2026, 10, 30)),
            Task("CS exam", 2, 3.0, date(2026, 11, 21))
            ]
    
    blocks = []

    result = unscheduled(tasks, blocks)

    assert len(result) == 2
    assert result[0].title == "DS exam"
    assert result[0].effort_h == tasks[0].effort_h
    assert result[1].title == "CS exam"
    assert result[1].effort_h == tasks[1].effort_h

def test_identical_tasks_independent_allocation():
    tasks = [
            Task("DS exam", 5, 6.0, date(2026, 10, 30)),
            Task("DS exam", 5, 6.0, date(2026, 10, 30)),
            ]
    blocks = [Block(tasks[0], 6.0)]

    result = unscheduled(tasks, blocks)

    assert len(result) == 1
    assert result[0] == tasks[1]
