from .models import Task


class InfeasiblePlan(Exception):
    needed_h: float
    available_h: float

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Store required and available study hours."""
        self.needed_h = needed_h
        self.available_h = available_h

    def __str__(self) -> str:
        return f"Needed {self.needed_h} hours, available {self.available_h} hours."


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Raise InfeasiblePlan if tasks exceed available hours."""
    needed_h = 0.0
    for task in tasks:
        needed_h += task.effort_h

    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
