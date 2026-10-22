from members.nhat_npm.w1.grades import summary
from members.nhat_npm.w1.text_tools import top_k
from members.nhat_npm.w1.rules import missing
from members.nhat_npm.w1.translate import binary_search
from members.nhat_npm.w1.timetable import by_day

def test_nhat_npm_grades():
    result = summary([1,2,2])

    assert result["min"] == 1
    assert result["max"] == 2
    assert result["mean"] == 1.67
    assert result["median"] == 2

def test_nhat_npm_text_tools():
    result = top_k("Banana,apple! BANANA; apple? cherry.", 10)

    assert result == [("apple", 2), ("banana", 2), ("cherry", 1)]

def test_nhat_npm_rules():
    result = missing(120, 1.5)

    assert len(result) == 1
    assert result[0] == "need GPA of at least 2.0"

def test_nhat_npm_binary_search():
    assert binary_search([-8, -3, 1, 5], -8) == 0
    assert binary_search([-8, -3, 1, 5], 5) == 3
    assert binary_search([-8, -3, 1, 5], 2) == -1

def test_nhat_npm_by_day():
    result = by_day([("CSC10014", "Thu"),
                     ("MTH00003", "Mon"),
                     ("CSC10014", "Mon"),
                     ("CSC10001", "Mon"),
                     ("PHY00001", "Thu")
                    ])

    assert result == {"Thu": ["CSC10014", "PHY00001"], "Mon": ["CSC10001", "CSC10014", "MTH00003"]}
