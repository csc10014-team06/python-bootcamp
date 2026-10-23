
def test_w1_1_summary_edge_case(load):
    g = load("w1", "grades")

    # EDGE CASE: All scores are identical.
    assert g.summary([4, 4, 4, 4]) == {
        "min": 4,
        "max": 4,
        "mean": 4,
        "median": 4,
    }


def test_w1_2_word_count_edge_case(load):
    t = load("w1", "text_tools")

    # EDGE CASE: Punctuation-only input contains no words.
    assert t.word_count("... !!! , ; ?") == {}
    assert t.top_k("... !!! , ; ?", 3) == []


def test_w1_3_thesis_edge_case(load):
    r = load("w1", "rules")

    # EDGE CASE: Exactly enough credits, but GPA is below the threshold.
    assert not r.can_register_thesis(120, 1.99)
    assert r.missing(120, 1.99) == ["GPA must be at least 2.0"]


def test_w1_4_gcd(load):
    tr = load("w1", "translate")

    assert tr.gcd(8, 15) == 1
    assert tr.gcd(0, 7) == 7
    assert tr.gcd(7, 0) == 7

    # EDGE CASE: Both inputs are zero.
    assert tr.gcd(0, 0) == 0

    # EDGE CASE: Consecutive Fibonacci numbers require multiple iterations.
    assert tr.gcd(55, 89) == 1

    assert tr.gcd(12, 12) == 12
    assert tr.gcd(84, 126) == 42

    # EDGE CASE: Python integers can exceed C++ long long limits.
    assert tr.gcd(10**100, 3 * 10**100) == 10**100


def test_w1_5_timetable_edge_case(load):
    tt = load("w1", "timetable")

    # EDGE CASE: The same course appears on different days.
    assert tt.by_day([
        ("CSC10014", "Tue"),
        ("CSC10014", "Mon"),
        ("CSC10001", "Tue"),
    ]) == {
        "Tue": ["CSC10001", "CSC10014"],
        "Mon": ["CSC10014"],
    }
