import argparse
import sys
from datetime import date

from .errors import InfeasiblePlan, check_feasible
from .io_utils import load_tasks, save_json


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m members.long_th.w2", description="Load tasks from CSV and check if the plan is feasible.")
    parser.add_argument("csv", help="path to the tasks CSV file")
    parser.add_argument("--hours", type=float, help="hours available for the plan")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(), help="reference date (YYYY-MM-DD), default is today")
    parser.add_argument("--out", help="save the loaded tasks to this JSON file")
    args = parser.parse_args(argv)

    try:
        tasks = load_tasks(args.csv)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    for t in tasks:
        print(f"{t.title}: importance {t.importance}, {t.effort_h} h, {t.days_left(args.today)} day(s) left")

    if args.hours is not None:
        try:
            check_feasible(tasks, args.hours)
        except InfeasiblePlan as e:
            print(e, file=sys.stderr)
            return 1
        print(f"Plan is feasible within {args.hours} h.")

    if args.out:
        save_json(tasks, args.out)
        print(f"Saved {len(tasks)} task(s) to {args.out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
