from members.truyen_lp.w1.grades import summary
from members.truyen_lp.w1.text_tools import top_k
from members.truyen_lp.w1.rules import missing
from members.truyen_lp.w1.translate import transpose
from members.truyen_lp.w1.timetable import by_day

def test_truyen_lp_grades():
    result = summary([1,2,2])

    assert result["min"] == 1
    assert result["max"] == 2
    assert result["mean"] == 1.67
    assert result["median"] == 2

def test_truyen_lp_text_tools():
    result = top_k("Banana,apple! BANANA; apple? cherry.", 10)

    assert result == [("apple", 2), ("banana", 2), ("cherry", 1)]

def test_truyen_lp_rules():
    result = missing(120, 1.5)

    assert len(result) == 1
    assert result[0] == "need 0.5 more GPA"

def test_truyen_lp_transpose():
    assert transpose([[1], [2], [3]]) == [[1, 2, 3]]
    assert transpose([[]]) == []

def test_truyen_lp_by_day():
    result = by_day([("CSC10014", "Thu"),
                     ("MTH00003", "Mon"),
                     ("CSC10014", "Mon"),
                     ("CSC10001", "Mon"),
                     ("PHY00001", "Thu")
                    ])

    assert result == {"Thu": ["CSC10014", "PHY00001"], "Mon": ["CSC10001", "CSC10014", "MTH00003"]}
