from shared.contract import Task, Block

def unscheduled(tasks: list[Task], blocks: list[Block]) -> list[Task]:
    remaining_tasks = []
    allocated_h = {}

    for block in blocks:
        key = id(block.task)
        allocated_h[key] = allocated_h.get(key, 0.0) + block.hours

    for task in tasks:
        remaining_h = task.effort_h - allocated_h.get(id(task), 0.0)

        if remaining_h > 0:
            remaining_tasks.append(Task(task.title, task.importance, remaining_h, task.deadline))

    return remaining_tasks
