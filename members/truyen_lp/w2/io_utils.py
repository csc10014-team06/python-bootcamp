import csv
import json
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    tasks: list[Task] = []
    with open(path, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):
            try:
                title = row["title"].strip()
                importance = int(row["importance"])
                effort_h = float(row["effort_h"])
                deadline = date.fromisoformat(row["deadline"].strip())
                task = Task(title=title, importance=importance, effort_h=effort_h, deadline=deadline)
            except (ValueError, TypeError, KeyError) as e:
                raise ValueError(f"Invalid task data on line {line_num}: {e}") from e
            tasks.append(task)
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    data = [
        {
            "title": t.title,
            "importance": t.importance,
            "effort_h": t.effort_h,
            "deadline": t.deadline.isoformat(),
        }
        for t in tasks
    ]
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
