"""Module for allocating study hours greedily to prioritised tasks."""

from shared.contract import Block, Task


def allocate(tasks: list[Task], hours: float) -> list[Block]:
    """Allocate available study hours greedily to tasks in the given order.

    Each task receives up to its effort_h, capped by remaining available hours.
    Returns a list of Block objects representing the scheduled study sessions.

    Args:
        tasks: List of Task objects (usually prioritised).
        hours: Total available study hours.

    Returns:
        List of Block objects with scheduled hours for each task.

    Raises:
        ValueError: If hours is negative.
    """
    if hours < 0:
        raise ValueError("Available hours cannot be negative")

    remaining = float(hours)
    blocks: list[Block] = []

    for task in tasks:
        if remaining <= 1e-9:
            break
        if task.effort_h <= 0:
            continue

        allocated_h = min(task.effort_h, remaining)
        blocks.append(Block(task=task, hours=allocated_h))
        remaining -= allocated_h

    return blocks
