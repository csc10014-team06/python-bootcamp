"""W2-3: Custom exception InfeasiblePlan and feasibility check."""

from collections.abc import Iterable

from .models import Task


class InfeasiblePlan(Exception):
    """Raised when total task effort exceeds available study hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(str(self))

    def __str__(self) -> str:
        return (
            f"Infeasible plan: needed {self.needed_h:.2f}h, "
            f"but only {self.available_h:.2f}h available."
        )


def check_feasible(tasks: Iterable[Task], available_h: float) -> bool:
    """Check if all tasks fit within available_h; raise InfeasiblePlan otherwise."""
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)
    return True