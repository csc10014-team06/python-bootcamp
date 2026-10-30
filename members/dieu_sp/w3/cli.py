"""W3-3: python -m members.dieu_sp.w3.cli tasks.csv --hours 2 [--today YYYY-MM-DD] prints a study plan."""

import argparse
import math
import sys
from datetime import date

from shared.study_planner.allocate import allocate
from shared.study_planner.leftover import unscheduled
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render
from shared.study_planner.validate import validate


def _hours(text: str) -> float:
    """argparse type for --hours: a positive, finite number of hours."""
    try:
        hours = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a number: {text!r}") from None
    if not math.isfinite(hours) or hours <= 0:
        raise argparse.ArgumentTypeError(f"must be a positive number: {text!r}")
    return hours


def _iso_date(text: str) -> date:
    """argparse type for --today: a date written as YYYY-MM-DD."""
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a YYYY-MM-DD date: {text!r}") from None


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the study-planner CLI."""
    parser = argparse.ArgumentParser(
        prog="python -m members.dieu_sp.w3.cli",
        description="Prioritise the tasks in a CSV and plan tonight's study hours.",
    )
    parser.add_argument("csv", help="tasks CSV with header title,importance,effort_h,deadline")
    parser.add_argument("--hours", type=_hours, required=True, help="hours available tonight")
    parser.add_argument("--today", type=_iso_date, default=None,
                        help="reference date YYYY-MM-DD (default: today)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run parse -> validate -> prioritise -> allocate -> render; return the exit code."""
    args = build_parser().parse_args(argv)
    today = args.today or date.today()

    try:
        tasks = parse_csv(args.csv)
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    errors = validate(tasks, today)
    if errors:
        for err in errors:
            print(f"Error: {err}", file=sys.stderr)
        return 1

    ordered = prioritise(tasks, today)
    blocks = allocate(ordered, args.hours)
    print(render(blocks))

    left = unscheduled(ordered, blocks)
    if left:
        print("Not scheduled tonight:")
        for t in left:
            print(f"- {t.title}: {t.effort_h:g} h left (due {t.deadline.isoformat()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
