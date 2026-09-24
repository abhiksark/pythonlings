from pathlib import Path

from pythonlings.core import curriculum


def test_source_root_finds_curriculum_files() -> None:
    root = curriculum.source_root()

    assert (root / "info.toml").exists()
    assert (root / "exercises").is_dir()
    assert (root / "checks").is_dir()


def test_init_workspace_copies_curriculum(tmp_path: Path) -> None:
    target = tmp_path / "workspace"

    result = curriculum.init_workspace(target)

    assert result == target.resolve()
    assert (target / "info.toml").exists()
    assert (target / "exercises").is_dir()
    assert (target / "checks").is_dir()
    assert (target / "solutions").is_dir()
    assert (target / ".pythonlings" / "originals").is_dir()
    assert (target / ".gitignore").read_text(encoding="utf-8").splitlines() == [
        ".pythonlings/state.json",
        ".pythonlings_debug.log",
        "__pycache__/",
        "*.pyc",
    ]


def test_init_workspace_refuses_non_empty_directory(tmp_path: Path) -> None:
    target = tmp_path / "workspace"
    target.mkdir()
    (target / "notes.txt").write_text("keep me", encoding="utf-8")

    try:
        curriculum.init_workspace(target)
    except curriculum.WorkspaceError as exc:
        assert "isn't empty and isn't a pythonlings workspace" in str(exc)
    else:
        raise AssertionError("expected WorkspaceError")


def test_force_init_preserves_existing_gitignore_entries(tmp_path: Path) -> None:
    target = tmp_path / "workspace"
    target.mkdir()
    gitignore = target / ".gitignore"
    original = "# Local ignores\n.env\n\n*.pyc"
    gitignore.write_text(original, encoding="utf-8")

    curriculum.init_workspace(target, force=True)

    expected = (
        original
        + "\n.pythonlings/state.json\n.pythonlings_debug.log\n__pycache__/\n"
    )
    assert gitignore.read_text(encoding="utf-8") == expected

    curriculum.init_workspace(target, force=True)

    assert gitignore.read_text(encoding="utf-8") == expected


def test_force_init_populates_empty_gitignore(tmp_path: Path) -> None:
    target = tmp_path / "workspace"
    target.mkdir()
    gitignore = target / ".gitignore"
    gitignore.touch()

    curriculum.init_workspace(target, force=True)

    assert gitignore.read_text(encoding="utf-8").splitlines() == curriculum.GITIGNORE_LINES


def test_force_init_preserves_gitignore_crlf_line_endings(tmp_path: Path) -> None:
    target = tmp_path / "workspace"
    target.mkdir()
    gitignore = target / ".gitignore"
    original = b"# Windows workspace\r\n.env"
    gitignore.write_bytes(original)

    curriculum.init_workspace(target, force=True)

    expected = original + b"\r\n" + b"\r\n".join(
        line.encode("utf-8") for line in curriculum.GITIGNORE_LINES
    ) + b"\r\n"
    assert gitignore.read_bytes() == expected


def test_update_workspace_preserves_user_exercise_edit(tmp_path: Path) -> None:
    target = curriculum.init_workspace(tmp_path / "workspace")
    exercise = next((target / "exercises").rglob("*.py"))
    exercise.write_text("# user edit\n", encoding="utf-8")

    curriculum.update_workspace(target)

    assert exercise.read_text(encoding="utf-8") == "# user edit\n"
    original = target / ".pythonlings" / "originals" / exercise.relative_to(target / "exercises")
    assert original.exists()
    assert (target / "solutions" / "_answers.py").exists()


def test_update_workspace_preserves_existing_gitignore_entries(tmp_path: Path) -> None:
    target = curriculum.init_workspace(tmp_path / "workspace")
    gitignore = target / ".gitignore"
    original = "# Team rules\n.coverage\n"
    gitignore.write_text(original, encoding="utf-8")

    curriculum.update_workspace(target)

    expected = original + "\n".join(curriculum.GITIGNORE_LINES) + "\n"
    assert gitignore.read_text(encoding="utf-8") == expected

    curriculum.update_workspace(target)

    assert gitignore.read_text(encoding="utf-8") == expected
