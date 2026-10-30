"""W3-3: Study-planner command-line tool.

Reuses the shared ``parse_csv`` from W2 and implements prioritise → allocate →
render as a self-contained CLI.

Usage::

    $ python -m members.long_th.w3.cli tasks.csv --hours 2 --today 2026-10-26
    Tonight (2.0 h):
      1. Assignment ...... 1.5 h
      2. DS exam ......... 0.5 h
"""

from __future__ import annotations

import argparse
import sys
from datetime import date

from shared.contract import Block, Task
from shared.study_planner.parse import parse_csv


# ---------------------------------------------------------------------------
# Pipeline helpers (Long's integration task)
# ---------------------------------------------------------------------------

def prioritise(tasks: list[Task], today: date) -> list[Task]:
    """Sort tasks by priority score descending (importance ÷ days_left).

    Tasks whose deadline has passed or is today get ``days_left = 0.5``
    (very urgent) to avoid division by zero.
    """
    def _score(t: Task) -> float:
        days_left = max((t.deadline - today).days, 0)
        if days_left == 0:
            days_left = 0.5  # overdue / due today → extremely urgent
        return t.importance / days_left

    return sorted(tasks, key=_score, reverse=True)


def allocate(tasks: list[Task], hours: float) -> list[Block]:
    """Greedily allocate tasks into the available *hours*.

    Each task is given as many hours as it needs (up to what remains).
    Partially-fitting tasks receive whatever time is left.
    """
    blocks: list[Block] = []
    remaining = hours
    for t in tasks:
        if remaining <= 0:
            break
        give = min(t.effort_h, remaining)
        blocks.append(Block(task=t, hours=give))
        remaining -= give
    return blocks


def render(blocks: list[Block]) -> str:
    """Render allocated blocks as a human-readable numbered list."""
    if not blocks:
        return "Nothing scheduled."
    total = sum(b.hours for b in blocks)
    lines: list[str] = [f"Tonight ({total:.1f} h):"]
    for i, b in enumerate(blocks, start=1):
        dots = "." * max(1, 20 - len(b.task.title))
        lines.append(f"  {i}. {b.task.title} {dots} {b.hours:.1f} h")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Parse arguments, run the pipeline, and print the study plan."""
    parser = argparse.ArgumentParser(
        prog="python -m members.long_th.w3.cli",
        description="Study-planner CLI — prioritise and schedule tasks.",
    )
    parser.add_argument("csv", help="path to the tasks CSV file")
    parser.add_argument(
        "--hours", type=float, required=True,
        help="hours available for tonight's session",
    )
    parser.add_argument(
        "--today", type=date.fromisoformat, default=date.today(),
        help="reference date YYYY-MM-DD (default: today)",
    )
    args = parser.parse_args(argv)

    # --- load ----------------------------------------------------------
    try:
        tasks = parse_csv(args.csv)
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not tasks:
        print("No tasks found in the CSV file.", file=sys.stderr)
        return 1

    # --- pipeline ------------------------------------------------------
    ordered = prioritise(tasks, args.today)
    blocks = allocate(ordered, args.hours)
    print(render(blocks))

    return 0


if __name__ == "__main__":
    sys.exit(main())

