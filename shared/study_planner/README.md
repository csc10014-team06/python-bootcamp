# Study Planner CLI

A command-line tool built as part of the team exercise (T-W3) to help students prioritise assignments and allocate daily study sessions efficiently based on urgency and importance.

---

## Architecture & Pipeline

The tool integrates modular components implemented across the team:

1. **`parse.py` (`parse_csv`)**: Loads and parses task records from a target CSV file into `Task` models.
2. **`validate.py` (`validate_tasks`)**: Verifies data integrity (positive effort hours, valid importance ratings 1–5, valid deadlines).
3. **`prioritise.py` (`prioritise`)**: Ranks tasks in descending order using the priority heuristic:
   $$\text{Priority} = \frac{\text{importance}}{\max(\text{days\_left}, 1)}$$
4. **`allocate.py` (`allocate`)**: Greedily fills available study hours into discrete study blocks.
5. **`render.py` (`render`)**: Formats allocated study blocks into a clean terminal report.
6. **`__main__.py`**: CLI orchestrator entry point built with standard library `argparse`.

---

## Installation & Environment

Ensure you have activated your project's virtual environment and installed all dependencies:

```bash
# Activate virtual environment
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\Activate.ps1      # Windows PowerShell

# Verify environment
python -m pip install -r requirements.txt

```

---

## CLI Usage

Run the package directly as an executable module:

```bash
python -m shared.study_planner <path_to_csv> --hours <available_hours> [--today <YYYY-MM-DD>]

```

### Positional Arguments

* `path_to_csv`: Relative or absolute file path to the task CSV file.

### Options

* `--hours <float>`: Total study time available in hours (e.g., `2.0`). Defaults to `2.0`.
* `--today <str>`: Reference evaluation date in ISO format (`YYYY-MM-DD`). Defaults to current local date (`date.today()`).

---

## Quick Example

Given a sample dataset `samples/tasks.csv`:

```bash
python -m shared.study_planner samples/tasks.csv --hours 2.0 --today 2026-10-26

```

**Expected output:**

```text
Tonight (2.0 h):
  1. Assignment ...... 1.5 h
  2. DS exam ......... 0.5 h

```

---

## Error Handling

The CLI gracefully handles edge cases and exits with standard non-zero exit codes (`code 1`):

* **Missing file**: Outputs `Error: file not found: <path>` to `stderr`.
* **Empty dataset**: Returns an informative message indicating no tasks are available for allocation.
* **Invalid date input**: Validates ISO date parsing format (`YYYY-MM-DD`) and prevents runtime panics.

---

## Testing

Run unit and integration test suites:

```bash
# Run bootcamp end-to-end tests
pytest -q python-bootcamp/tests/test_w3.py

# Lint check codebase
ruff check python-bootcamp/shared/study_planner

```
