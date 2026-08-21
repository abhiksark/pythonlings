from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _make_workspace(root: Path) -> Path:
    (root / "exercises" / "variables").mkdir(parents=True)
    (root / "checks" / "variables").mkdir(parents=True)
    (root / "solutions").mkdir()
    (root / ".pythonlings" / "originals" / "variables").mkdir(parents=True)
    (root / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "variables1"\n'
        'path = "exercises/variables/variables1.py"\n'
        'hint = "Use an assignment."\n'
        'docs = "https://docs.python.org/3/tutorial/introduction.html"\n',
        encoding="utf-8",
    )
    exercise = "# I AM NOT DONE\nanswer = 0\n"
    (root / "exercises" / "variables" / "variables1.py").write_text(
        exercise, encoding="utf-8"
    )
    (root / "checks" / "variables" / "variables1.py").write_text(
        "assert answer == 42\n", encoding="utf-8"
    )
    (root / "solutions" / "variables1.py").write_text(
        "answer = 42\n", encoding="utf-8"
    )
    (
        root
        / ".pythonlings"
        / "originals"
        / "variables"
        / "variables1.py"
    ).write_text(exercise, encoding="utf-8")
    return root


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pythonlings", *args],
        cwd=cwd,
        env=os.environ.copy(),
        capture_output=True,
        text=True,
    )


def _tree_snapshot(root: Path) -> list[tuple[str, str, bytes | str]]:
    snapshot: list[tuple[str, str, bytes | str]] = []
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            snapshot.append((relative, "symlink", os.readlink(path)))
        elif path.is_file():
            snapshot.append((relative, "file", path.read_bytes()))
        elif path.is_dir():
            snapshot.append((relative, "directory", ""))
    return snapshot


def test_doctor_reports_a_healthy_workspace(tmp_path: Path) -> None:
    root = _make_workspace(tmp_path / "healthy")
    before = _tree_snapshot(root)

    result = _run("--root", str(root), "doctor")

    assert result.returncode == 0, result.stderr
    assert f"Workspace: {root.resolve()}" in result.stdout
    assert "[OK] Manifest: 1 exercises across 1 topics" in result.stdout
    assert "0 failure(s)" in result.stdout
    assert _tree_snapshot(root) == before


def test_doctor_warning_does_not_fail_or_modify_state(tmp_path: Path) -> None:
    root = _make_workspace(tmp_path / "warning")
    state_path = root / ".pythonlings" / "state.json"
    state_path.write_text("not json {{", encoding="utf-8")
    before = state_path.read_bytes()

    result = _run("--root", str(root), "doctor")

    assert result.returncode == 0, result.stderr
    assert "[WARN] Progress state:" in result.stdout
    assert state_path.read_bytes() == before
    assert not state_path.with_suffix(".json.bak").exists()


def test_doctor_required_failure_is_friendly(tmp_path: Path) -> None:
    root = tmp_path / "not-a-workspace"
    root.mkdir()

    result = _run("--root", str(root), "doctor")

    assert result.returncode == 1
    assert "[FAIL] Workspace:" in result.stdout
    assert "[FAIL] Manifest:" in result.stdout
    assert "Traceback" not in result.stdout + result.stderr


def test_doctor_malformed_manifest_is_friendly(tmp_path: Path) -> None:
    root = tmp_path / "malformed-manifest"
    (root / "exercises").mkdir(parents=True)
    (root / "checks").mkdir()
    (root / "info.toml").write_text("[[exercises\n", encoding="utf-8")

    result = _run("--root", str(root), "doctor")

    assert result.returncode == 1
    assert "[OK] Workspace:" in result.stdout
    assert "[FAIL] Manifest:" in result.stdout
    assert "Traceback" not in result.stdout + result.stderr


def test_doctor_rejects_non_string_manifest_fields(tmp_path: Path) -> None:
    for field, replacement in (
        ('name = "variables1"', "name = 123"),
        (
            'docs = "https://docs.python.org/3/tutorial/introduction.html"',
            "docs = 123",
        ),
    ):
        root = _make_workspace(tmp_path / field.split()[0])
        info = root / "info.toml"
        info.write_text(
            info.read_text(encoding="utf-8").replace(field, replacement),
            encoding="utf-8",
        )

        result = _run("--root", str(root), "doctor")

        assert result.returncode == 1
        assert "[FAIL] Manifest:" in result.stdout
        assert "Traceback" not in result.stdout + result.stderr


def test_doctor_rejects_exercise_and_check_directories(tmp_path: Path) -> None:
    root = _make_workspace(tmp_path / "directory-paths")
    exercise = root / "exercises" / "variables" / "variables1.py"
    check = root / "checks" / "variables" / "variables1.py"
    exercise.unlink()
    check.unlink()
    exercise.mkdir()
    check.mkdir()

    result = _run("--root", str(root), "doctor")

    assert result.returncode == 1
    assert "[FAIL] Manifest:" in result.stdout
    assert "is not a file" in result.stdout
    assert "Traceback" not in result.stdout + result.stderr


def test_doctor_symlink_loop_is_friendly(tmp_path: Path) -> None:
    root = tmp_path / "workspace-loop"
    root.symlink_to(root)

    result = _run("--root", str(root), "doctor")

    assert result.returncode == 1
    assert "[FAIL] Workspace:" in result.stdout
    assert "check the path and symlinks" in result.stdout
    assert "Traceback" not in result.stdout + result.stderr


def test_doctor_unknown_home_user_is_friendly() -> None:
    root = "~pythonlings_no_such_user_93847/work"

    result = _run("--root", root, "doctor")

    assert result.returncode == 1
    assert "[FAIL] Workspace:" in result.stdout
    # POSIX leaves an unknown ~user unexpanded, so the path stays literal and
    # doctor reports it as unresolvable. Windows expands it to a path under the
    # users directory, which is merely missing. Both are correct, so assert what
    # holds either way -- a reported failure naming the user -- rather than
    # pinning one platform's wording.
    assert "pythonlings_no_such_user_93847" in result.stdout
    assert "Traceback" not in result.stdout + result.stderr


def test_doctor_is_listed_in_cli_help() -> None:
    result = _run("--help")

    assert result.returncode == 0
    assert "doctor" in result.stdout


def test_doctor_honors_explicit_root_over_current_workspace(tmp_path: Path) -> None:
    current = _make_workspace(tmp_path / "current")
    explicit = _make_workspace(tmp_path / "explicit")

    result = _run("--root", str(explicit), "doctor", cwd=current)

    assert result.returncode == 0, result.stderr
    assert f"Workspace: {explicit.resolve()}" in result.stdout
    assert f"Workspace: {current.resolve()}" not in result.stdout


def test_doctor_does_not_migrate_legacy_state_or_write_debug_log(
    tmp_path: Path,
) -> None:
    root = _make_workspace(tmp_path / "legacy")
    current_state = root / ".pythonlings"
    legacy_state = root / ".pylings"
    current_state.rename(legacy_state)
    before = {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }

    result = _run("--debug", "--root", str(root), "doctor")

    after = {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }
    assert result.returncode == 0, result.stderr
    assert before == after
    assert legacy_state.is_dir()
    assert not current_state.exists()
    assert not (root / ".pythonlings_debug.log").exists()
