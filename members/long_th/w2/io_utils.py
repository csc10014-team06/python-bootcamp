from datetime import date
from typing import List
import csv
import json
from .models import Task


def load_tasks(path) -> List[Task]:
    tasks = []
    with open(path, newline="", encoding="utf-8") as f:
        for i,row in enumerate(csv.DictReader(f),start=2):
            if (row["title"] == '' or row["importance"] == '' or row["effort_h"] == '' or row["deadline"] == ''):
                raise ValueError(f"Empty value on line {i}")
            try:
                task = Task(
                    title=row["title"],
                    importance=int(row["importance"]),
                    effort_h=float(row["effort_h"]),
                    deadline=date.fromisoformat(row["deadline"]),
                )
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid value on line {i}: {e}")
            tasks.append(task)
    return tasks


def save_json(tasks, path):
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
        json.dump(data, f, ensure_ascii = False, indent = 4)
