# tests/integration/test_cli_run.py
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pythonlings", *args],
        capture_output=True,
        text=True,
    )


def test_run_passing_exercise_exits_zero() -> None:
    result = _run("--root", str(FIXTURES), "run", "passing")
    assert result.returncode == 0
    assert "passing" in result.stdout


def test_run_failing_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "run", "asserts")
    assert result.returncode != 0
    assert "AssertionError" in (result.stdout + result.stderr)


def test_run_pending_marker_shows_nudge() -> None:
    result = _run("--root", str(FIXTURES), "run", "pending")
    # exit 0 from the script but the marker blocks pass.
    assert result.returncode != 0
    assert "I AM NOT DONE" in (result.stdout + result.stderr)


def test_run_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "run", "nope")
    assert result.returncode != 0
    assert "nope" in result.stderr


@pytest.mark.parametrize("command", ["run", "dry-run", "verify", "solution"])
def test_invalid_utf8_exercise_reports_error_without_traceback(
    tmp_path: Path, command: str
) -> None:
    root = tmp_path / "work"
    shutil.copytree(FIXTURES.parent / "passing_curriculum", root)
    directory = "solutions" if command == "solution" else "exercises"
    (root / directory).mkdir(exist_ok=True)
    invalid_path = root / directory / "passing1.py"
    invalid_path.write_bytes(b"\xff")
    args = [command]
    if command != "verify":
        args.append("passing1")

    result = _run("--root", str(root), *args)

    assert result.returncode == 1
    assert "UTF-8" in result.stderr
    assert str(invalid_path) in result.stderr
    assert "Traceback" not in result.stderr
    assert invalid_path.read_bytes() == b"\xff"
