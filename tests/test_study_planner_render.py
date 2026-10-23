from datetime import date

from shared.contract import Block, Task
from shared.study_planner.render import render

DS = Task("DS exam", 5, 6.0, date(2026, 10, 30))
HW = Task("Assignment", 4, 1.5, date(2026, 10, 27))


def test_render_full_plan():
    assert render([Block(DS, 6.0), Block(HW, 1.5)]) == (
        "Study plan:\n"
        "1. DS exam - 6 h (importance 5, due 2026-10-30)\n"
        "2. Assignment - 1.5 h (importance 4, due 2026-10-27)\n"
        "Total: 7.5 h"
    )


def test_render_partial_block():
    out = render([Block(DS, 2.0)])
    assert "1. DS exam - 2 of 6 h" in out
    assert out.endswith("Total: 2 h")


def test_render_empty():
    assert render([]) == "No study blocks planned."


def test_render_keeps_block_order():
    lines = render([Block(HW, 1.5), Block(DS, 6.0)]).splitlines()
    assert lines[1].startswith("1. Assignment")
    assert lines[2].startswith("2. DS exam")


def test_render_total_float_sum():
    t = Task("Read", 2, 0.3, date(2026, 11, 1))
    assert render([Block(t, 0.1), Block(t, 0.2)]).endswith("Total: 0.3 h")
