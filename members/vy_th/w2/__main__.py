from .io_utils import load_tasks

tasks = load_tasks("samples/tasks.csv")

for task in tasks:
    print(task)
