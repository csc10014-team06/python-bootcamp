import csv
from datetime import date
import json
from pathlib import Path
from typing import List, Union
from .models import Task


def load_tasks(path: Union[str, Path]) -> List[Task]:
    tasks = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        _ = next(reader, None)  
        line_no = 1  

        for row in reader:
            line_no += 1

            if not row or not any(field.strip() for field in row):
                continue

            try:
                if len(row) != 4:
                    raise ValueError("Row must contain exactly 4 columns")

                title = row[0].strip()
                importance = int(row[1])
                effort_h = float(row[2])
                deadline = date.fromisoformat(row[3].strip())

                task = Task(title, importance, effort_h, deadline)
                tasks.append(task)
            except Exception as e:
                raise ValueError(f"Invalid row at line {line_no}: {e}") from e

    return tasks


def save_json(tasks: List[Task], path: Union[str, Path]) -> None:
    tasks_data = []
    for t in tasks:
        tasks_data.append({
            "title": t.title,
            "importance": t.importance,
            "effort_h": t.effort_h,
            "deadline": t.deadline.isoformat(),  
        })

    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(tasks_data, f, indent=2, ensure_ascii=False)