from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from shared.contract import Block, Task

try:
    from shared.study_planner.parse import parse_csv
except ImportError:
    import csv

    def parse_csv(path: str | Path) -> list[Task]:
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


try:
    from shared.study_planner.validate import validate
except ImportError:
    def validate(tasks: list[Task], today: date) -> list[str]:
        errors: list[str] = []
        for t in tasks:
            if not 1 <= t.importance <= 5:
                errors.append(f"Task '{t.title}': importance {t.importance} must be between 1 and 5")
            if t.effort_h < 0:
                errors.append(f"Task '{t.title}': effort_h {t.effort_h} cannot be negative")
        return errors


try:
    from shared.study_planner.prioritise import prioritise
except ImportError:
    def prioritise(tasks: list[Task], today: date) -> list[Task]:
        return sorted(
            tasks,
            key=lambda t: t.importance / max(1, (t.deadline - today).days),
            reverse=True,
        )


try:
    from shared.study_planner.allocate import allocate
except ImportError:
    def allocate(tasks: list[Task], hours: float) -> list[Block]:
        if hours < 0:
            raise ValueError("Available hours cannot be negative")
        remaining = float(hours)
        blocks: list[Block] = []
        for t in tasks:
            if remaining <= 1e-9:
                break
            if t.effort_h <= 0:
                continue
            alloc = min(t.effort_h, remaining)
            blocks.append(Block(task=t, hours=alloc))
            remaining -= alloc
        return blocks


try:
    from shared.study_planner.render import render
except ImportError:
    def render(blocks: list[Block]) -> str:
        total_h = sum(b.hours for b in blocks)
        lines = [f"Tonight ({total_h:.1f} h):"]
        for idx, b in enumerate(blocks, start=1):
            dots = "." * max(2, 22 - len(b.task.title))
            lines.append(f"  {idx}. {b.task.title} {dots} {b.hours:.1f} h")
        return "\n".join(lines)


try:
    from shared.study_planner.leftover import unscheduled
except ImportError:
    def unscheduled(tasks: list[Task], blocks: list[Block]) -> list[Task]:
        allocated_h: dict[int, float] = {}
        for b in blocks:
            allocated_h[id(b.task)] = allocated_h.get(id(b.task), 0.0) + b.hours
        leftovers: list[Task] = []
        for t in tasks:
            rem = t.effort_h - allocated_h.get(id(t), 0.0)
            if rem > 1e-9:
                leftovers.append(Task(t.title, t.importance, rem, t.deadline))
        return leftovers


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="study-planner")
    parser.add_argument("path")
    parser.add_argument("--hours", type=float, default=2.0)
    parser.add_argument("--today", type=str, default=None)

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 2

    csv_path = Path(args.path)
    if not csv_path.is_file():
        print(f"Error: file not found: {args.path}", file=sys.stderr)
        return 1

    if args.hours < 0:
        print(f"Error: hours cannot be negative: {args.hours}", file=sys.stderr)
        return 1

    if args.today:
        try:
            today_date = date.fromisoformat(args.today)
        except ValueError as err:
            print(f"Error: invalid --today date format: {err}", file=sys.stderr)
            return 1
    else:
        today_date = date.today()

    try:
        tasks = parse_csv(csv_path)
    except (ValueError, OSError, KeyError) as err:
        print(f"Error parsing tasks CSV: {err}", file=sys.stderr)
        return 1

    validation_errors = validate(tasks, today_date)
    if validation_errors:
        for err in validation_errors:
            print(f"Validation error: {err}", file=sys.stderr)
        return 1

    prioritised = prioritise(tasks, today_date)
    blocks = allocate(prioritised, args.hours)
    plan_output = render(blocks)
    print(plan_output)

    _ = unscheduled(prioritised, blocks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
