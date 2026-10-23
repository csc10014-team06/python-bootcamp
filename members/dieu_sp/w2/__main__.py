"""W2-5: python -m members.dieu_sp.w2 [csv] prints the tasks in a CSV (default: samples/tasks.csv)."""

import sys
from datetime import date
from pathlib import Path

from .io_utils import load_tasks

SAMPLE = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    path = args[0] if args else SAMPLE
    try:
        tasks = load_tasks(path)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    today = date.today()
    for t in tasks:
        print(
            f"{t.title}: importance {t.importance}, {t.effort_h:g} h, "
            f"due {t.deadline.isoformat()} ({t.days_left(today)} day(s) left)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
