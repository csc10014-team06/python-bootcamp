"""W2-2: Load tasks from CSV and save them as JSON."""

import csv
import json
from datetime import date

from .models import Task

COLUMNS = ["title", "importance", "effort_h", "deadline"]


def load_tasks(path) -> list[Task]:
    """Read a CSV with header title,importance,effort_h,deadline into a list of Task.

    An invalid row raises ValueError with its line number.
    """
    tasks = []
    with open(path, newline="", encoding="utf-8") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            try:
                tasks.append(Task(
                    title=row["title"].strip(),
                    importance=int(row["importance"]),
                    effort_h=float(row["effort_h"]),
                    deadline=date.fromisoformat(row["deadline"].strip()),
                ))
            except (KeyError, TypeError, AttributeError, ValueError) as e:
                raise ValueError(f"Invalid row on line {line}: {e}") from e
    return tasks


def save_json(tasks: list[Task], path) -> None:
    """Write tasks to path as a JSON list, with deadlines as YYYY-MM-DD."""
    data = [
        {
            "title": t.title,
            "importance": t.importance,
            "effort_h": t.effort_h,
            "deadline": t.deadline.isoformat(),
        }
        for t in tasks
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
