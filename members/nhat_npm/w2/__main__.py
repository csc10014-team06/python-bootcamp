
from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    """Load and print the sample tasks."""
    sample_csv = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"
    tasks = load_tasks(sample_csv)

    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()
