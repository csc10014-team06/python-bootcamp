"""Command-line study planner for a task CSV."""

import argparse
import sys
from datetime import date
from math import isfinite
from pathlib import Path

from members.nhat_npm.w2.io_utils import load_tasks
from members.nhat_npm.w2.models import Task


def build_plan(tasks: list[Task], hours: float, today: date) -> list[tuple[Task, float]]:
    """Prioritize tasks and allocate up to ``hours`` of study time."""
    prioritised = sorted(
        tasks,
        key=lambda task: task.importance / max(1, task.days_left(today)),
        reverse=True,
    )
    remaining = hours
    plan: list[tuple[Task, float]] = []

    for task in prioritised:
        if remaining <= 0:
            break
        if task.effort_h <= 0:
            continue

        allocated = min(task.effort_h, remaining)
        plan.append((task, allocated))
        remaining -= allocated

    return plan


def render_plan(plan: list[tuple[Task, float]]) -> str:
    """Format allocated tasks as a numbered evening study plan."""
    total_hours = sum(hours for _, hours in plan)
    lines = [f"Tonight ({total_hours:.1f} h):"]

    for number, (task, hours) in enumerate(plan, start=1):
        dots = "." * max(2, 22 - len(task.title))
        lines.append(f"  {number}. {task.title} {dots} {hours:.1f} h")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Run the study planner CLI and return its process exit code."""
    parser = argparse.ArgumentParser(description="Plan study time from a tasks CSV.")
    parser.add_argument("path", type=Path, help="path to a tasks CSV file")
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="positive number of available study hours",
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        metavar="YYYY-MM-DD",
        help="date used to calculate task priority (default: today)",
    )
    args = parser.parse_args(argv)

    if not args.path.is_file():
        print(f"Error: file not found: {args.path}", file=sys.stderr)
        return 1
    if not isfinite(args.hours) or args.hours <= 0:
        print("Error: --hours must be a finite number greater than zero.", file=sys.stderr)
        return 1

    try:
        tasks = load_tasks(args.path)
    except (OSError, ValueError) as exc:
        print(f"Error: could not load tasks: {exc}", file=sys.stderr)
        return 1

    print(render_plan(build_plan(tasks, args.hours, args.today)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
