from datetime import date

from shared.contract import Task


def prioritise(tasks: list[Task], today: date) -> list[Task]:
    """
    Sort tasks by priority, calculated as importance / days_left.

    Tasks due today or overdue use 1 as the minimum divisor,
    avoiding division by zero and giving urgent tasks higher priority.
    """
    return sorted(
        tasks,
        key=lambda task: task.importance
        / max(1, (task.deadline - today).days),
        reverse=True,
    )