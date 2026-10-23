from datetime import date
from dataclasses import dataclass

@dataclass
class Task:
    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self):
        if not (1 <= self.importance <= 5):
            raise ValueError("importance must be between 1-5")

    def days_left(self, today: date) -> int:
        if (self.deadline < today):
            return 0
        return (self.deadline - today).days