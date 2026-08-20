# tests/unit/test_manifest.py
from pathlib import Path

import pytest

from pythonlings.core.manifest import Manifest, ManifestError, load

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _write_curriculum(
    root: Path, name: str, exercise_src: str = "", check_src: str = ""
) -> None:
    """Write a minimal one-exercise curriculum under `root`."""
    (root / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        f'name = "{name}"\n'
        f'path = "exercises/{name}.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    (root / "exercises").mkdir(exist_ok=True)
    (root / "exercises" / f"{name}.py").write_text(exercise_src, encoding="utf-8")
    (root / "checks").mkdir(exist_ok=True)
    (root / "checks" / f"{name}.py").write_text(check_src, encoding="utf-8")


def test_load_tiny_curriculum() -> None:
    manifest = load(FIXTURES)
    assert isinstance(manifest, Manifest)
    assert [ex.name for ex in manifest.exercises] == [
        "passing",
        "asserts",
        "syntax",
        "pending",
    ]
    assert manifest.welcome_message == "Welcome to the test curriculum."
    assert manifest.final_message == "All test exercises complete."
    assert manifest.exercises[0].topic == "exercises"
    assert manifest.exercises[0].hint.startswith("This one should always pass")


def test_check_path_is_derived() -> None:
    manifest = load(FIXTURES)
    check = manifest.by_name("passing").check_path
    assert check == FIXTURES / "checks" / "passing.py"


def test_load_defaults_messages_when_omitted(tmp_path: Path) -> None:
    _write_curriculum(tmp_path, "a")
    manifest = load(tmp_path)
    assert manifest.welcome_message == "Welcome to pythonlings!"
    assert manifest.final_message == "All exercises complete."


def test_load_optional_docs_url(tmp_path: Path) -> None:
    _write_curriculum(tmp_path, "a")
    info_path = tmp_path / "info.toml"
    info_path.write_text(
        info_path.read_text(encoding="utf-8")
        + 'docs = "https://docs.python.org/3/tutorial/introduction.html"\n',
        encoding="utf-8",
    )
    manifest = load(tmp_path)
    assert (
        manifest.by_name("a").docs
        == "https://docs.python.org/3/tutorial/introduction.html"
    )


def test_load_rejects_missing_info_toml(tmp_path: Path) -> None:
    with pytest.raises(ManifestError, match="info.toml"):
        load(tmp_path)


def test_load_rejects_wrong_format_version(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text("format_version = 2\n", encoding="utf-8")
    with pytest.raises(ManifestError, match="format_version"):
        load(tmp_path)


def test_load_rejects_empty_exercises_list(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text("format_version = 1\n", encoding="utf-8")
    with pytest.raises(ManifestError, match="non-empty"):
        load(tmp_path)


def test_load_rejects_missing_exercise_path(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/missing.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    # The message echoes the path with the platform's separator.
    with pytest.raises(ManifestError, match=r"exercises[\\/]missing\.py"):
        load(tmp_path)


def test_load_rejects_path_not_under_exercises(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "lessons/a.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="under exercises/"):
        load(tmp_path)


def test_load_rejects_missing_check_file(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/a.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "a.py").write_text("", encoding="utf-8")
    # No checks/a.py created.
    with pytest.raises(ManifestError, match="check file"):
        load(tmp_path)


def test_load_rejects_duplicate_names(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        '[[exercises]]\nname = "a"\npath = "exercises/a.py"\nhint = "h"\n'
        '[[exercises]]\nname = "a"\npath = "exercises/b.py"\nhint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "exercises" / "b.py").write_text("", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "checks" / "b.py").write_text("", encoding="utf-8")
    with pytest.raises(ManifestError, match="duplicate"):
        load(tmp_path)


def test_manifest_by_name_and_index_of() -> None:
    manifest = load(FIXTURES)
    assert manifest.by_name("asserts").name == "asserts"
    assert manifest.index_of("syntax") == 2
    with pytest.raises(KeyError):
        manifest.by_name("nope")


def test_topics_in_first_appearance_order() -> None:
    manifest = load(FIXTURES)
    # tiny_curriculum's exercises all live directly under exercises/,
    # so they share the single topic "exercises".
    assert manifest.topics() == ["exercises"]


def test_exercises_in_returns_topic_members_in_order() -> None:
    manifest = load(FIXTURES)
    names = [ex.name for ex in manifest.exercises_in("exercises")]
    assert names == ["passing", "asserts", "syntax", "pending"]


def test_exercises_in_unknown_topic_is_empty() -> None:
    manifest = load(FIXTURES)
    assert manifest.exercises_in("nope") == []


def test_real_curriculum_has_roadmap_topic_counts() -> None:
    repo = Path(__file__).parents[2]
    manifest = load(repo)
    expected = {
        "itertools": 8,
        "json": 8,
        "datetime": 8,
        "enums": 6,
        "pathlib": 6,
        "oop_advanced": 12,
        "async": 10,
    }
    assert len(manifest.exercises) == 292
    assert len(manifest.topics()) == 31
    for topic, count in expected.items():
        assert len(manifest.exercises_in(topic)) == count


def test_real_curriculum_exercises_have_official_docs_links() -> None:
    repo = Path(__file__).parents[2]
    manifest = load(repo)
    missing = [exercise.name for exercise in manifest.exercises if not exercise.docs]
    assert missing == []
    assert all(
        exercise.docs.startswith("https://docs.python.org/3/")
        for exercise in manifest.exercises
    )


def test_real_curriculum_check_files_parse() -> None:
    import ast

    repo = Path(__file__).parents[2]
    manifest = load(repo)
    for exercise in manifest.exercises:
        ast.parse(
            exercise.check_path.read_text(encoding="utf-8"),
            filename=str(exercise.check_path),
        )


def test_load_rejects_invalid_toml_syntax(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text("format_version = [1\n", encoding="utf-8")
    with pytest.raises(ManifestError, match=r"info\.toml"):
        load(tmp_path)


def test_load_rejects_invalid_utf8(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_bytes(b"\xff")
    with pytest.raises(ManifestError, match="valid UTF-8"):
        load(tmp_path)


def test_load_wraps_info_toml_read_errors(tmp_path: Path) -> None:
    (tmp_path / "info.toml").mkdir()
    with pytest.raises(ManifestError, match=r"could not read info\.toml"):
        load(tmp_path)


def test_load_rejects_missing_name_field(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'path = "exercises/a.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="'name'"):
        load(tmp_path)


def test_load_rejects_wrong_type_name_field(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        "name = 123\n"
        'path = "exercises/a.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="'name'"):
        load(tmp_path)


def test_load_rejects_missing_path_field(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="'path'"):
        load(tmp_path)


def test_load_rejects_absolute_path(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "/etc/passwd"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="under exercises/"):
        load(tmp_path)


def test_load_rejects_traversal_path(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/../../etc/passwd"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="under exercises/"):
        load(tmp_path)


def test_load_rejects_symlink_escape(tmp_path: Path) -> None:
    """A path that is lexically clean (no '..', not absolute, starts with
    exercises/) can still resolve outside the workspace via a symlink, e.g.
    exercises/link/secret.py where "link" is a symlink to somewhere else.
    The lexical checks alone don't catch this -- containment must be
    verified against the *resolved* path.
    """
    outside = tmp_path.parent / "outside_workspace"
    outside.mkdir(exist_ok=True)
    (outside / "secret.py").write_text("SECRET = 1\n", encoding="utf-8")

    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "link").symlink_to(outside, target_is_directory=True)
    (tmp_path / "checks").mkdir()

    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/link/secret.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="escapes the workspace"):
        load(tmp_path)


def test_load_rejects_check_symlink_escape(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}_outside_checks"
    outside.mkdir()
    (outside / "a.py").write_text("assert True\n", encoding="utf-8")

    (tmp_path / "exercises" / "topic").mkdir(parents=True)
    (tmp_path / "exercises" / "topic" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "topic").symlink_to(outside, target_is_directory=True)
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/topic/a.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )

    with pytest.raises(ManifestError, match=r"check path.*escapes the workspace"):
        load(tmp_path)


def test_load_rejects_top_level_exercises_symlink_escape(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside_exercises"
    workspace.mkdir()
    outside.mkdir()
    (outside / "a.py").write_text("", encoding="utf-8")
    (workspace / "exercises").symlink_to(outside, target_is_directory=True)
    (workspace / "checks").mkdir()
    (workspace / "checks" / "a.py").write_text("", encoding="utf-8")
    (workspace / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/a.py"\n',
        encoding="utf-8",
    )

    with pytest.raises(ManifestError, match="exercises/ directory escapes"):
        load(workspace)


def test_load_rejects_top_level_checks_symlink_escape(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside_checks"
    workspace.mkdir()
    outside.mkdir()
    (outside / "a.py").write_text("", encoding="utf-8")
    (workspace / "checks").symlink_to(outside, target_is_directory=True)
    (workspace / "exercises").mkdir()
    (workspace / "exercises" / "a.py").write_text("", encoding="utf-8")
    (workspace / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/a.py"\n',
        encoding="utf-8",
    )

    with pytest.raises(ManifestError, match="checks/ directory escapes"):
        load(workspace)


def test_load_rejects_directory_exercise_path(tmp_path: Path) -> None:
    (tmp_path / "exercises" / "topic").mkdir(parents=True)
    (tmp_path / "checks" / "topic").mkdir(parents=True)
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/topic"\n',
        encoding="utf-8",
    )

    with pytest.raises(ManifestError, match="exercise path is not a file"):
        load(tmp_path)


def test_load_rejects_directory_check_path(tmp_path: Path) -> None:
    (tmp_path / "exercises" / "topic").mkdir(parents=True)
    (tmp_path / "exercises" / "topic" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "checks" / "topic" / "a.py").mkdir(parents=True)
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/topic/a.py"\n',
        encoding="utf-8",
    )

    with pytest.raises(ManifestError, match="path is not a file"):
        load(tmp_path)


def test_load_wraps_symlink_resolution_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    exercise_path = tmp_path / "exercises" / "a.py"
    _write_curriculum(tmp_path, "a")
    original_resolve = Path.resolve

    def fail_exercise_resolution(path: Path, strict: bool = False) -> Path:
        if path == exercise_path:
            raise RuntimeError("symlink loop")
        return original_resolve(path, strict=strict)

    monkeypatch.setattr(Path, "resolve", fail_exercise_resolution)

    with pytest.raises(ManifestError, match="could not resolve exercise path"):
        load(tmp_path)


@pytest.mark.parametrize("field", ["hint", "docs"])
def test_load_rejects_non_string_exercise_text(tmp_path: Path, field: str) -> None:
    _write_curriculum(tmp_path, "a")
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/a.py"\n'
        f"{field} = 1\n",
        encoding="utf-8",
    )

    with pytest.raises(ManifestError, match=field):
        load(tmp_path)


@pytest.mark.parametrize("field", ["welcome_message", "final_message"])
def test_load_rejects_non_string_manifest_text(tmp_path: Path, field: str) -> None:
    _write_curriculum(tmp_path, "a")
    info_path = tmp_path / "info.toml"
    info_path.write_text(
        f"{field} = 1\n" + info_path.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    with pytest.raises(ManifestError, match=field):
        load(tmp_path)
