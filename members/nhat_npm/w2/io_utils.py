
import csv
import json
from datetime import date
from os import PathLike

from .models import Task


def load_tasks(path: str | PathLike[str]) -> list[Task]:
    """Load and validate tasks from a CSV file."""
    tasks = []

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "title",
            "importance",
            "effort_h",
            "deadline",
        }

        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError("CSV must contain title, importance, effort_h, deadline headers")

        for line_number, row in enumerate(reader, start=2):
            try:
                title = row["title"].strip()
                importance = int(row["importance"])
                effort_h = float(row["effort_h"])
                deadline = date.fromisoformat(row["deadline"])

                if not title:
                    raise ValueError("title cannot be empty")

                task = Task(
                    title=title,
                    importance=importance,
                    effort_h=effort_h,
                    deadline=deadline,
                )

                tasks.append(task)

            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(
                    f"Invalid row at line {line_number}: {exc}"
                ) from exc

    return tasks


def save_json(tasks: list[Task], path: str | PathLike[str]) -> None:
    """Save tasks as an indented JSON array."""
    data = [
        {
            "title": task.title,
            "importance": task.importance,
            "effort_h": task.effort_h,
            "deadline": task.deadline.isoformat(),
        }
        for task in tasks
    ]

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
