"""shared/contract.py

Team code contract for exercises T-W2 and T-W3.
Defines shared interfaces and Task contract.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """A study task read from tasks.csv (title,importance,effort_h,deadline).

    Holds values only; range checks (e.g. importance 1-5) belong in validate.py.
    """
    title: str
    importance: int
    effort_h: float
    deadline: date


@dataclass
class Block:
    """A slice of study time allocated to a task."""
    task: Task
    hours: float
