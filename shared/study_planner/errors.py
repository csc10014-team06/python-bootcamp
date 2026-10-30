"""Error handling module for Study Planner (Team T-W3, Member 3: M.Nhật).

Provides:
- InfeasiblePlan exception
- File validation (missing file, empty CSV)
- Feasibility checking against available study hours
- Comprehensive error validation utilities
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from shared.contract import Task


class InfeasiblePlan(Exception):
    """Raised when required study effort exceeds available hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        self.needed_h = float(needed_h)
        self.available_h = float(available_h)
        super().__init__(str(self))

    def __str__(self) -> str:
        return (
            f"Infeasible plan: needed {self.needed_h:.1f} h, "
            f"but only {self.available_h:.1f} h available."
        )


class EmptyCSVError(ValueError):
    """Raised when a tasks CSV file has no records."""


def check_file(path: str | Path) -> Path:
    """Validate that the file exists and is not empty.

    Args:
        path: File path to inspect.

    Returns:
        Resolved Path object.

    Raises:
        FileNotFoundError: If the file does not exist.
        EmptyCSVError: If the file is 0 bytes or has only a header without data rows.
    """
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"Tasks file not found: {path}")

    if file_path.stat().st_size == 0:
        raise EmptyCSVError(f"Tasks CSV file is completely empty: {path}")

    with file_path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            raise EmptyCSVError(f"Tasks CSV file contains no header or content: {path}")

        first_row = next(reader, None)
        if first_row is None:
            raise EmptyCSVError(f"Tasks CSV file has a header but no task rows: {path}")

    return file_path


def check_feasible(tasks: Iterable[Task], available_h: float) -> bool:
    """Check if all tasks fit within available_h.

    Args:
        tasks: Iterable of Task objects.
        available_h: Total study hours available.

    Returns:
        True if total required hours <= available_h.

    Raises:
        ValueError: If available_h is negative.
        InfeasiblePlan: If total effort exceeds available_h.
    """
    if available_h < 0:
        raise ValueError(f"Available hours cannot be negative: {available_h}")

    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)

    return True


def validate_input(
    csv_path: str | Path,
    available_h: float,
    today: date | None = None,
) -> list[str]:
    """Validate all study planner inputs and collect human-readable error messages.

    Args:
        csv_path: Path to tasks CSV.
        available_h: Available hours.
        today: Reference date for deadlines (optional).

    Returns:
        List of error message strings (empty if everything is valid).
    """
    errors: list[str] = []

    # 1. Check file existence and content
    try:
        check_file(csv_path)
    except (FileNotFoundError, EmptyCSVError) as exc:
        errors.append(str(exc))
        return errors

    # 2. Check available hours
    if available_h < 0:
        errors.append(f"Available hours cannot be negative: {available_h}")

    return errors
