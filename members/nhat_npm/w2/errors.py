
from collections.abc import Iterable

from .models import Task


class InfeasiblePlan(Exception):
    """Error raised when requested study hours cannot fit the plan."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Store the required and available study time."""
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(self.__str__())

    def __str__(self) -> str:
        """Return a readable explanation of the infeasible plan."""
        return (
            f"Plan is infeasible: need {self.needed_h} hours, "
            f"but only {self.available_h} hours are available."
        )


def check_feasible(tasks: Iterable[Task], available_h: float) -> None:
    """Raise ``InfeasiblePlan`` when tasks need more than available hours."""
    needed_h = sum(task.effort_h for task in tasks)

    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
