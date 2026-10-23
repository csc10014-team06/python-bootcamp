"""W2-3: Custom exception for a plan that does not fit the available hours."""

from .models import Task


class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float):
        super().__init__(needed_h, available_h)
        self.needed_h = needed_h
        self.available_h = available_h

    def __str__(self) -> str:
        return f"Plan needs {self.needed_h:g} h but only {self.available_h:g} h are available"


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Raise InfeasiblePlan if the total effort of tasks exceeds available_h."""
    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
