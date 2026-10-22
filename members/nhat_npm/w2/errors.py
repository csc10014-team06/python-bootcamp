
class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float):
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return (
            f"Plan is infeasible: need {self.needed_h} hours, "
            f"but only {self.available_h} hours are available."
        )


def check_feasible(tasks, available_h: float) -> None:
    needed_h = sum(task.effort_h for task in tasks)

    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
