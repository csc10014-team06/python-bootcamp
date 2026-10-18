"""W2-1: Task model using dataclass."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represents a study task with importance, effort in hours, and deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("title must not be empty")
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5")
        if self.effort_h <= 0:
            raise ValueError("effort_h must be positive")

    def days_left(self, today: date) -> int:
        """Return the number of days remaining until the deadline (never below 0)."""
        return max(0, (self.deadline - today).days)