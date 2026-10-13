"""shared/contract.py

Team code contract for exercises T-W2 and T-W3.
Defines shared interfaces and Task contract.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a shared task item for team exercises."""
    id: int
    title: str
    description: str = ""
    completed: bool = False
    assigned_to: str | None = None
