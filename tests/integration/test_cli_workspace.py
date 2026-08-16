from pathlib import Path

from pythonlings.cli import main


_STALE_CHECK = "# stale check used to identify the updated workspace\n"


def _stale_workspace(root: Path) -> Path:
    assert main(["init", "--path", str(root)]) == 0
    check = next((root / "checks").rglob("*.py"))
    check.write_text(_STALE_CHECK, encoding="utf-8")
    return check


def _assert_updated(check: Path) -> None:
    assert check.read_text(encoding="utf-8") != _STALE_CHECK


def _assert_not_updated(check: Path) -> None:
    assert check.read_text(encoding="utf-8") == _STALE_CHECK


def test_init_command_creates_workspace(tmp_path: Path) -> None:
    target = tmp_path / "learn-python"

    code = main(["init", "--path", str(target)])

    assert code == 0
    assert (target / "info.toml").exists()
    assert (target / "exercises").is_dir()
    assert (target / "checks").is_dir()
    assert (target / ".gitignore").read_text(encoding="utf-8").splitlines() == [
        ".pythonlings/state.json",
        ".pythonlings_debug.log",
        "__pycache__/",
        "*.pyc",
    ]


def test_init_rejects_non_empty_non_workspace_dir(tmp_path: Path, capsys) -> None:
    target = tmp_path / "stuff"
    target.mkdir()
    (target / "notes.txt").write_text("keep", encoding="utf-8")

    code = main(["init", "--path", str(target)])

    assert code == 1
    err = capsys.readouterr().err
    assert "isn't empty and isn't a pythonlings workspace" in err


def test_init_on_existing_workspace_is_friendly_noop(tmp_path: Path, capsys) -> None:
    target = tmp_path / "ws"
    assert main(["init", "--path", str(target)]) == 0
    capsys.readouterr()  # discard first output

    code = main(["init", "--path", str(target)])

    assert code == 0
    assert "Already set up" in capsys.readouterr().out


def test_init_force_overwrites_existing_workspace(tmp_path: Path) -> None:
    target = tmp_path / "ws"
    target.mkdir()
    gitignore = target / ".gitignore"
    gitignore.write_text("# Local ignores\n.venv/\n", encoding="utf-8")

    code = main(["init", "--path", str(target), "--force"])

    assert code == 0
    assert (target / "info.toml").exists()
    assert gitignore.read_text(encoding="utf-8") == (
        "# Local ignores\n.venv/\n"
        ".pythonlings/state.json\n"
        ".pythonlings_debug.log\n"
        "__pycache__/\n"
        "*.pyc\n"
    )


def test_update_via_path_migrates_legacy_state_dir(tmp_path: Path) -> None:
    target = tmp_path / "legacy-ws"
    main(["init", "--path", str(target)])
    (target / ".pythonlings").rename(target / ".pylings")
    (target / ".pylings" / "state.json").write_text(
        '{"format_version": 2, "completed": ["variables1"], "seen_intro": true,'
        ' "last_topic": "variables", "last_exercise": "variables2"}',
        encoding="utf-8",
    )

    # --path points at the workspace; cwd is elsewhere. The legacy dir must move.
    main(["update", "--path", str(target)])

    assert not (target / ".pylings").exists()
    assert (target / ".pythonlings" / "state.json").exists()
    from pythonlings.core.state import load as load_state

    assert "variables1" in load_state(target).completed


def test_update_command_preserves_user_exercises(tmp_path: Path) -> None:
    target = tmp_path / "learn-python"
    assert main(["init", "--path", str(target)]) == 0
    exercise = next((target / "exercises").rglob("*.py"))
    exercise.write_text("# edited\n", encoding="utf-8")
    gitignore = target / ".gitignore"
    gitignore.write_text("# Team rules\n.coverage\n", encoding="utf-8")

    code = main(["update", "--path", str(target)])

    assert code == 0
    assert exercise.read_text(encoding="utf-8") == "# edited\n"
    assert (target / ".pythonlings" / "originals").is_dir()
    assert gitignore.read_text(encoding="utf-8") == (
        "# Team rules\n.coverage\n"
        ".pythonlings/state.json\n"
        ".pythonlings_debug.log\n"
        "__pycache__/\n"
        "*.pyc\n"
    )


def test_update_path_takes_precedence_over_root_and_cwd(
    tmp_path: Path, monkeypatch
) -> None:
    cwd = tmp_path / "cwd-ws"
    root = tmp_path / "root-ws"
    path = tmp_path / "path-ws"
    cwd_check = _stale_workspace(cwd)
    root_check = _stale_workspace(root)
    path_check = _stale_workspace(path)
    monkeypatch.chdir(cwd)

    code = main(
        [
            "--root",
            str(root),
            "update",
            "--path",
            str(path),
        ]
    )

    assert code == 0
    _assert_updated(path_check)
    _assert_not_updated(root_check)
    _assert_not_updated(cwd_check)


def test_update_root_takes_precedence_over_cwd(tmp_path: Path, monkeypatch) -> None:
    cwd = tmp_path / "cwd-ws"
    root = tmp_path / "root-ws"
    cwd_check = _stale_workspace(cwd)
    root_check = _stale_workspace(root)
    monkeypatch.chdir(cwd)

    code = main(["--root", str(root), "update"])

    assert code == 0
    _assert_updated(root_check)
    _assert_not_updated(cwd_check)


def test_bare_update_prefers_current_workspace(tmp_path: Path, monkeypatch) -> None:
    home = tmp_path / "home-ws"
    monkeypatch.setenv("PYTHONLINGS_HOME", str(home))
    home_check = _stale_workspace(home)
    cwd = tmp_path / "cwd-ws"
    cwd_check = _stale_workspace(cwd)
    monkeypatch.chdir(cwd)

    code = main(["update"])

    assert code == 0
    _assert_updated(cwd_check)
    _assert_not_updated(home_check)


def test_bare_update_uses_home_workspace_outside_workspace(
    tmp_path: Path, monkeypatch
) -> None:
    home = tmp_path / "home-ws"
    monkeypatch.setenv("PYTHONLINGS_HOME", str(home))
    home_check = _stale_workspace(home)
    outside = tmp_path / "outside"
    outside.mkdir()
    monkeypatch.chdir(outside)

    code = main(["update"])

    assert code == 0
    _assert_updated(home_check)


def test_update_missing_path_fails_without_creating_it(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    target = tmp_path / "missing"
    outside = tmp_path / "outside"
    outside.mkdir()
    monkeypatch.setenv("PYTHONLINGS_HOME", str(target))
    monkeypatch.chdir(outside)

    code = main(["update"])

    assert code == 1
    assert "is not a pythonlings workspace" in capsys.readouterr().err
    assert not target.exists()


def test_update_non_workspace_fails_without_modifying_it(
    tmp_path: Path, capsys
) -> None:
    target = tmp_path / "not-a-workspace"
    target.mkdir()
    marker = target / "keep.txt"
    marker.write_text("keep\n", encoding="utf-8")

    code = main(["update", "--path", str(target)])

    assert code == 1
    assert "is not a pythonlings workspace" in capsys.readouterr().err
    assert list(target.iterdir()) == [marker]
    assert marker.read_text(encoding="utf-8") == "keep\n"
