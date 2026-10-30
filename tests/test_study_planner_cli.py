"""End-to-end tests for the shared study planner command-line interface."""

import subprocess
import sys
from pathlib import Path

BOOTCAMP = Path(__file__).resolve().parents[1]


def test_cli_builds_a_study_plan_from_sample_csv() -> None:
    """Run the CLI as a process and check its plan for the sample tasks."""
    sample_csv = BOOTCAMP / "samples" / "tasks.csv"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "shared.study_planner.cli",
            str(sample_csv),
            "--hours",
            "2",
            "--today",
            "2026-10-26",
        ],
        capture_output=True,
        text=True,
        cwd=BOOTCAMP,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Study plan:" in result.stdout
    assert "Assignment - 1.5 h" in result.stdout
    assert "DS exam - 0.5 of 6 h" in result.stdout
    assert "Total: 2 h" in result.stdout
