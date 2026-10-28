"""End-to-end integration tests for shared.study_planner CLI (T-W3)."""

from pathlib import Path
import subprocess
import sys

BOOTCAMP = Path(__file__).resolve().parents[1]
SAMPLE_CSV = BOOTCAMP / "samples" / "tasks.csv"


def test_study_planner_e2e_success() -> None:
    """Test running study_planner via -m with a valid sample CSV and --today."""
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "shared.study_planner",
            str(SAMPLE_CSV),
            "--hours",
            "2",
            "--today",
            "2026-10-26",
        ],
        capture_output=True,
        text=True,
        cwd=str(BOOTCAMP),
    )
    assert proc.returncode == 0
    assert "Assignment" in proc.stdout
    assert "DS exam" in proc.stdout
    assert "Total: 2 h" in proc.stdout


def test_study_planner_e2e_missing_file() -> None:
    """Test running study_planner with a non-existent file."""
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "shared.study_planner",
            "non_existent.csv",
            "--hours",
            "2",
        ],
        capture_output=True,
        text=True,
        cwd=str(BOOTCAMP),
    )
    assert proc.returncode != 0
    assert "not found" in proc.stderr.lower() or proc.returncode == 1


def test_study_planner_e2e_negative_hours() -> None:
    """Test running study_planner with negative hours."""
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "shared.study_planner",
            str(SAMPLE_CSV),
            "--hours",
            "-1",
            "--today",
            "2026-10-26",
        ],
        capture_output=True,
        text=True,
        cwd=str(BOOTCAMP),
    )
    assert proc.returncode != 0
    assert "negative" in proc.stderr.lower()
