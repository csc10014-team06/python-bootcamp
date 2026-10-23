from datetime import date

from shared.contract import Task
from shared.study_planner.prioritise import prioritise


TODAY = date(2026, 10, 23)


def make_task(title, importance, days):
    return Task(
        title=title,
        importance=importance,
        effort_h=1.0,
        deadline=date.fromordinal(TODAY.toordinal() + days),
    )


def test_prioritise_by_importance_and_deadline():
    tasks = [
        make_task("Project", 5, 10),
        make_task("Exam", 5, 2),
        make_task("Assignment", 4, 4),
        make_task("Reading", 2, 1),
    ]

    result = prioritise(tasks, TODAY)

    assert [task.title for task in result] == [
        "Exam",
        "Reading",
        "Assignment",
        "Project",
    ]


def test_prioritise_due_today():
    tasks = [
        make_task("Later", 5, 5),
        make_task("Due today", 3, 0),
    ]

    # EDGE CASE: A zero-day deadline must not cause division by zero.
    result = prioritise(tasks, TODAY)

    assert [task.title for task in result] == [
        "Due today",
        "Later",
    ]


def test_prioritise_overdue_task():
    tasks = [
        make_task("Upcoming", 5, 2),
        make_task("Overdue", 4, -3),
    ]

    # EDGE CASE: Overdue tasks use the minimum divisor of 1.
    result = prioritise(tasks, TODAY)

    assert [task.title for task in result] == [
        "Overdue",
        "Upcoming",
    ]


def test_prioritise_empty_list():
    # EDGE CASE: No tasks should return an empty list.
    assert prioritise([], TODAY) == []


def test_prioritise_equal_priorities_preserves_order():
    tasks = [
        make_task("First", 2, 2),
        make_task("Second", 4, 4),
    ]

    # EDGE CASE: Equal priority scores preserve input order.
    result = prioritise(tasks, TODAY)

    assert [task.title for task in result] == [
        "First",
        "Second",
    ]


def test_prioritise_does_not_modify_original_list():
    tasks = [
        make_task("Low priority", 1, 10),
        make_task("High priority", 5, 1),
    ]
    original = tasks.copy()

    result = prioritise(tasks, TODAY)

    assert tasks == original
    assert result is not tasks