import csv
from datetime import date

from shared.contract import Task

COLUMNS = ["title", "importance", "effort_h", "deadline"]


def parse_csv(path) -> list[Task]:
    """Read a tasks CSV (title,importance,effort_h,deadline) into a list of Task.

    Only checks that each value has the right type. Range checks such as
    importance 1-5 are left to validate.py.
    Raises ValueError with the line number if a row cannot be parsed.
    """
    tasks = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing column(s): {', '.join(missing)}")

        for i, row in enumerate(reader, start=2):
            values = {c: (row[c] or "").strip() for c in COLUMNS}
            if any(v == "" for v in values.values()):
                raise ValueError(f"Empty value on line {i}")
            try:
                task = Task(
                    title=values["title"],
                    importance=int(values["importance"]),
                    effort_h=float(values["effort_h"]),
                    deadline=date.fromisoformat(values["deadline"]),
                )
            except ValueError as e:
                raise ValueError(f"Invalid value on line {i}: {e}") from e
            tasks.append(task)
    return tasks
