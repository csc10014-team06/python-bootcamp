# Study Planner CLI Walkthrough & Demo

This document demonstrates the execution workflow, expected output format, and error handling for the integrated `shared.study_planner` CLI tool.

---

## Environment Preparation

Verify your environment setup and ensure the package dependencies are properly loaded:

```bash
# Verify Python version
python --version

# Ensure dependencies are installed
pip install -r requirements.txt

```

### Sample Dataset

The walkthrough uses `samples/tasks.csv`:

```csv
title,importance,effort_h,deadline
Assignment,5,1.5,2026-10-27
DS exam,4,3.0,2026-10-30
Read paper,2,1.0,2026-11-05

```

---

## Scenarios

### Scenario 1: Standard Daily Planning (Happy Path)

Allocate 2.0 hours of available study time using a reference date:

```bash
python -m shared.study_planner samples/tasks.csv --hours 2.0 --today 2026-10-26

```

**Expected Output:**

```text
Tonight (2.0 h):
  1. Assignment ...... 1.5 h
  2. DS exam ......... 0.5 h

```

**Calculation Breakdown:**

* `Assignment`: $\text{days\_left} = 1$, score = $5 / 1 = 5.0$. Takes 1.5 h.
* `DS exam`: $\text{days\_left} = 4$, score = $4 / 4 = 1.0$. Receives remaining 0.5 h (out of 3.0 h needed).
* `Read paper`: Not reached due to the 2.0-hour cap.

---

### Scenario 2: Larger Study Window

Allocate 4.0 hours to accommodate more workload:

```bash
python -m shared.study_planner samples/tasks.csv --hours 4.0 --today 2026-10-26

```

**Expected Output:**

```text
Tonight (4.0 h):
  1. Assignment ...... 1.5 h
  2. DS exam ......... 2.5 h

```

---

### Scenario 3: Missing CSV File

Run the CLI pointing to a file path that does not exist:

```bash
python -m shared.study_planner non_existent.csv --hours 2.0

```

**Expected Output (`stderr`):**

```text
Error: file not found: non_existent.csv

```

**Exit Code:** `1`

---

### Scenario 4: Malformed Date String

Run the CLI with an invalid format for `--today`:

```bash
python -m shared.study_planner samples/tasks.csv --hours 2.0 --today 26-10-2026

```

**Expected Output (`stderr`):**

```text
Error: invalid date format for --today: 26-10-2026

```

**Exit Code:** `1`

---

## Quality Verification

Run automated test suites and style linters:

```bash
# Run Week 3 test suite
pytest -q tests/test_w3.py

# Run Ruff code analysis
ruff check shared/study_planner

```