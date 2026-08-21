from __future__ import annotations

from pathlib import Path

from pythonlings.core.doctor import CheckStatus, run_diagnostics


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


def _result(report, name: str):
    return next(check for check in report.checks if check.name == name)


def test_healthy_workspace_has_no_warnings_or_failures(tmp_path: Path) -> None:
    root = _make_workspace(tmp_path)

    report = run_diagnostics(root, package_version="0.4.1")

    assert report.has_failures is False
    assert all(check.status is CheckStatus.OK for check in report.checks)


def test_corrupt_state_is_a_warning_and_is_not_modified(tmp_path: Path) -> None:
    root = _make_workspace(tmp_path)
    state_path = root / ".pythonlings" / "state.json"
    state_path.write_text("not json {{", encoding="utf-8")
    before = state_path.read_bytes()

    report = run_diagnostics(root, package_version="0.4.1")

    assert report.has_failures is False
    assert _result(report, "Progress state").status is CheckStatus.WARNING
    assert state_path.read_bytes() == before
    assert not state_path.with_suffix(".json.bak").exists()


def test_missing_workspace_is_a_required_failure(tmp_path: Path) -> None:
    root = tmp_path / "missing"

    report = run_diagnostics(root, package_version="0.4.1")

    assert report.has_failures is True
    assert _result(report, "Workspace").status is CheckStatus.FAILURE
    assert _result(report, "Manifest").status is CheckStatus.FAILURE
    assert not root.exists()


def test_missing_solution_is_a_warning(tmp_path: Path) -> None:
    root = _make_workspace(tmp_path)
    (root / "solutions" / "variables1.py").unlink()

    report = run_diagnostics(root, package_version="0.4.1")

    result = _result(report, "Solutions")
    assert report.has_failures is False
    assert result.status is CheckStatus.WARNING
    assert "variables1" in result.message
    assert "pythonlings update" in result.message


def test_missing_snapshot_is_an_actionable_warning(tmp_path: Path) -> None:
    root = _make_workspace(tmp_path)
    (
        root
        / ".pythonlings"
        / "originals"
        / "variables"
        / "variables1.py"
    ).unlink()

    report = run_diagnostics(root, package_version="0.4.1")

    result = _result(report, "Reset snapshots")
    assert report.has_failures is False
    assert result.status is CheckStatus.WARNING
    assert "pythonlings update" in result.message


def test_bundled_docs_error_is_an_actionable_warning(
    tmp_path: Path, monkeypatch
) -> None:
    root = _make_workspace(tmp_path)

    def fail_to_load(*args, **kwargs):
        raise PermissionError("permission denied")

    monkeypatch.setattr("pythonlings.core.doctor.load_snippet", fail_to_load)

    report = run_diagnostics(root, package_version="0.4.1")

    result = _result(report, "Bundled docs")
    assert report.has_failures is False
    assert result.status is CheckStatus.WARNING
    assert "reinstall pythonlings" in result.message


def test_dangling_state_symlink_is_a_warning(tmp_path: Path) -> None:
    root = _make_workspace(tmp_path)
    state_path = root / ".pythonlings" / "state.json"
    state_path.symlink_to(root / "missing-state.json")

    report = run_diagnostics(root, package_version="0.4.1")

    result = _result(report, "Progress state")
    assert result.status is CheckStatus.WARNING
    assert "broken symlink" in result.message
