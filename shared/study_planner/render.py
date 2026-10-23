from shared.contract import Block


def render(blocks: list[Block]) -> str:
    """Return a readable study plan: one numbered line per block, then the total hours.

    A block that covers only part of a task shows "<hours> of <effort_h> h".
    An empty list returns "No study blocks planned."
    """
    if not blocks:
        return "No study blocks planned."

    lines = ["Study plan:"]
    for i, block in enumerate(blocks, start=1):
        task = block.task
        hours = f"{block.hours:g} h"
        if block.hours < task.effort_h:
            hours = f"{block.hours:g} of {task.effort_h:g} h"
        lines.append(
            f"{i}. {task.title} - {hours} "
            f"(importance {task.importance}, due {task.deadline.isoformat()})"
        )
    total = sum(block.hours for block in blocks)
    lines.append(f"Total: {total:g} h")
    return "\n".join(lines)
