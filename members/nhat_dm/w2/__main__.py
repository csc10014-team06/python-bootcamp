"""W2-5: Entry point for `python -m members.<you>.w2`."""

import sys
from pathlib import Path

from .io_utils import load_tasks


def _find_default_csv() -> Path:
    """Locate sample tasks.csv in common bootcamp paths."""
    candidates = [
        Path("samples/tasks.csv"),
        Path("python-bootcamp/samples/tasks.csv"),
        Path(__file__).resolve().parents[3] / "samples" / "tasks.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def main(argv: list[str] | None = None) -> int:
    """Load sample CSV and print tasks."""
    args = argv if argv is not None else sys.argv[1:]
    csv_path = Path(args[0]) if args else _find_default_csv()

    tasks = load_tasks(csv_path)
    for idx, task in enumerate(tasks, start=1):
        print(
            f"{idx}. {task.title} "
            f"(importance={task.importance}, effort={task.effort_h}h, "
            f"deadline={task.deadline.isoformat()})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())