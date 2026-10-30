from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys

from members.han_htg.w2.io_utils import load_tasks
from members.han_htg.w2.models import Task


def get_priority(task: Task, today: date) -> float:
    """Calculate priority score (importance / days_left)."""
    days = task.days_left(today)
    return task.importance / max(days, 1)


def main(argv: list[str] | None = None) -> None:
    """CLI entrypoint for planning study sessions."""
    parser = argparse.ArgumentParser(description="Study planner CLI")
    parser.add_argument("path", help="Path to tasks CSV file")
    parser.add_argument("--hours", type=float, default=2.0, help="Available study hours (default: 2.0)")
    parser.add_argument("--today", type=str, default=None, help="Reference date in YYYY-MM-DD format")

    args = parser.parse_args(argv)

    csv_path = Path(args.path)
    if not csv_path.is_file():
        sys.stderr.write(f"Error: file not found: {args.path}\n")
        sys.exit(1)

    if args.today:
        try:
            today = date.fromisoformat(args.today)
        except ValueError as err:
            sys.stderr.write(f"Error: invalid date format: {err}\n")
            sys.exit(1)
    else:
        today = date.today()

    try:
        tasks = load_tasks(csv_path)
    except Exception as err:
        sys.stderr.write(f"Error loading tasks: {err}\n")
        sys.exit(1)

    sorted_tasks = sorted(tasks, key=lambda t: get_priority(t, today), reverse=True)

    rem_hours = args.hours
    blocks: list[tuple[str, float]] = []
    for task in sorted_tasks:
        if rem_hours <= 0:
            break
        alloc = min(task.effort_h, rem_hours)
        if alloc > 0:
            blocks.append((task.title, alloc))
            rem_hours -= alloc

    print(f"Tonight ({args.hours:.1f} h):")
    for idx, (title, hours) in enumerate(blocks, start=1):
        dots_count = max(3, 20 - len(title))
        dots = "." * dots_count
        print(f"  {idx}. {title} {dots} {hours:.1f} h")


if __name__ == "__main__":
    main()