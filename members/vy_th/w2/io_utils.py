import csv
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load and validate tasks from a CSV file."""
    tasks = []

    with open(path, newline="", encoding="utf-8") as f:
        data = csv.DictReader(f)

        for line_num, row in enumerate(data, start=2):
            try:
                if None in row:
                    raise ValueError("extra column")

                title = row["title"]
                if title is None or not title.strip():
                    raise ValueError("empty title")

                importance = int(row["importance"])
                effort_h = float(row["effort_h"])
                deadline = date.fromisoformat(row["deadline"])

                task = Task(title, importance, effort_h, deadline)

                tasks.append(task)
            except (ValueError, TypeError, KeyError) as e:
                raise ValueError(f"line {line_num}: {e}") from e

    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Save tasks to a JSON file."""
    data = []

    for task in tasks:
        item = asdict(task)
        item["deadline"] = task.deadline.isoformat()

        data.append(item)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
