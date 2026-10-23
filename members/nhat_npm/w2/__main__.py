
from pathlib import Path

from .io_utils import load_tasks


def main():
    sample_csv = Path(__file__).parent / "tasks.csv"
    tasks = load_tasks(sample_csv)

    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()
