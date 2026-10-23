from datetime import date
from typing import List

from shared.contract import Task


def validate(tasks: List[Task], today: date) -> List[str]:
    errors = []

    if not tasks:
        return ["Tasks list cannot be empty"]

    seen_titles = set()

    for idx, t in enumerate(tasks, start=1):
        if not t.title or not t.title.strip():
            errors.append(f"Task {idx}: Title cannot be empty")

        if t.title in seen_titles:
            errors.append(f"Task {idx}: Duplicate task title '{t.title}'")
        else:
            seen_titles.add(t.title)

        if not 1 <= t.importance <= 5:
            errors.append(f"Task {idx} ('{t.title}'): Importance must be between 1 and 5")

        if t.effort_h <= 0:
            errors.append(f"Task {idx} ('{t.title}'): Effort hours must be greater than 0")

        if t.deadline < today:
            errors.append(f"Task {idx} ('{t.title}'): Deadline {t.deadline} is already overdue as of {today}")

    return errors