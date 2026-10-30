import argparse
import sys
from datetime import date
from pathlib import Path

from members.vy_th.w2.io_utils import load_tasks


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily study planner")

    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--hours", type=float, required=True)
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Reference date in YYYY-MM-DD format",
    )

    args = parser.parse_args()

    if args.hours <= 0:
        parser.error("--hours must be positive")

    try:
        tasks = load_tasks(args.csv_file)
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv_file}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: invalid CSV data: {exc}", file=sys.stderr)
        return 1

    def priority(task):
        days_left = max((task.deadline - args.today).days, 1)
        return task.importance / days_left

    tasks = sorted(tasks, key=priority, reverse=True)

    remaining = args.hours
    scheduled = []

    for task in tasks:
        if remaining <= 0:
            break

        allocated = min(task.effort_h, remaining)

        if allocated > 0:
            scheduled.append((task.title, allocated))
            remaining -= allocated

    print(f"Tonight ({args.hours:.1f} h):")

    for index, (title, hours) in enumerate(scheduled, start=1):
        print(f"  {index}. {title:.<20} {hours:.1f} h")

    if not scheduled:
        print("  No tasks scheduled.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
