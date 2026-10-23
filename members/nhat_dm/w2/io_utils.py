"""W2-2: Load tasks from CSV and save tasks to JSON."""

import csv
import json
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load a list of Task objects from a CSV file.

    Raises ValueError with the line number if a row is invalid.
    """
    file_path = Path(path)
    tasks: list[Task] = []

    with file_path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        expected_fields = {"title", "importance", "effort_h", "deadline"}
        if reader.fieldnames is None or not expected_fields.issubset(set(reader.fieldnames)):
            raise ValueError("Line 1: Invalid or missing CSV header")

        # Dòng 1 là header, dữ liệu bắt đầu từ dòng 2
        for line_no, row in enumerate(reader, start=2):
            try:
                if None in row.values() or any(v is None for v in row.values()):
                    raise ValueError("Missing column values")

                title = row["title"].strip()
                importance = int(row["importance"])
                effort_h = float(row["effort_h"])
                deadline = date.fromisoformat(row["deadline"].strip())

                task = Task(
                    title=title,
                    importance=importance,
                    effort_h=effort_h,
                    deadline=deadline,
                )
                tasks.append(task)
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"Invalid row at line {line_no}: {exc}") from exc

    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Save a list of Task objects to a JSON file."""
    file_path = Path(path)
    data = [
        {
            "title": task.title,
            "importance": task.importance,
            "effort_h": task.effort_h,
            "deadline": task.deadline.isoformat(),
        }
        for task in tasks
    ]
    with file_path.open(mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)