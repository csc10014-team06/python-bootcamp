import sys
from pathlib import Path

from .io_utils import load_tasks


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if argv:
        csv_path = Path(argv[0])
    else:
        csv_path = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"

    if not csv_path.exists():
        print(f"Error: file not found: {csv_path}", file=sys.stderr)
        return 1

    try:
        tasks = load_tasks(csv_path)
    except (ValueError, OSError) as err:
        print(f"Error loading tasks: {err}", file=sys.stderr)
        return 1

    for t in tasks:
        print(f"- {t.title}: importance={t.importance}, effort={t.effort_h}h, deadline={t.deadline}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
