"""W3-3: Command-line tool for scheduling study sessions."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

try:
    from members.truyen_lp.w2.io_utils import load_tasks
    from members.truyen_lp.w2.models import Task
except ImportError:
    import csv
    from dataclasses import dataclass

    @dataclass
    class Task:  # type: ignore[no-redef]
        title: str
        importance: int
        effort_h: float
        deadline: date

        def days_left(self, today: date) -> int:
            return max((self.deadline - today).days, 0)

    def load_tasks(path: str | Path) -> list[Task]:  # type: ignore[no-redef]
        tasks: list[Task] = []
        with open(path, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append(
                    Task(
                        title=row["title"].strip(),
                        importance=int(row["importance"]),
                        effort_h=float(row["effort_h"]),
                        deadline=date.fromisoformat(row["deadline"].strip()),
                    )
                )
        return tasks


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for study session scheduling."""
    parser = argparse.ArgumentParser(
        prog="cli",
        description="Schedule study sessions from a tasks CSV file.",
    )
    parser.add_argument("path", help="Path to tasks CSV file")
    parser.add_argument(
        "--hours",
        type=float,
        default=2.0,
        help="Available study hours tonight (default: 2.0)",
    )
    parser.add_argument(
        "--today",
        type=str,
        default=None,
        help="Date to calculate urgency against in YYYY-MM-DD format (default: today)",
    )

    args = parser.parse_args(argv)

    csv_path = Path(args.path)
    if not csv_path.is_file():
        sys.stderr.write(f"Error: file not found: {args.path}\n")
        return 1

    if args.hours < 0:
        sys.stderr.write(f"Error: hours cannot be negative: {args.hours}\n")
        return 1

    if args.today:
        try:
            today_date = date.fromisoformat(args.today.strip())
        except ValueError as exc:
            sys.stderr.write(f"Error: invalid date format for --today: {exc}\n")
            return 1
    else:
        today_date = date.today()

    try:
        tasks = load_tasks(csv_path)
    except (ValueError, OSError, KeyError) as exc:
        sys.stderr.write(f"Error loading tasks CSV: {exc}\n")
        return 1

    prioritised = sorted(
        tasks,
        key=lambda t: t.importance / max(t.days_left(today_date), 1),
        reverse=True,
    )

    remaining = float(args.hours)
    blocks: list[tuple[Task, float]] = []
    for task in prioritised:
        if remaining <= 1e-9:
            break
        if task.effort_h <= 0:
            continue
        alloc = min(task.effort_h, remaining)
        blocks.append((task, alloc))
        remaining -= alloc

    print(f"Tonight ({args.hours:.1f} h):")
    for idx, (task, alloc) in enumerate(blocks, start=1):
        dots = "." * max(2, 16 - len(task.title))
        print(f"  {idx}. {task.title} {dots} {alloc:.1f} h")

    return 0


if __name__ == "__main__":
    sys.exit(main())
