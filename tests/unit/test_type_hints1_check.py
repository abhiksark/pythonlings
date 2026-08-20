# tests/unit/test_type_hints1_check.py

from pathlib import Path

from pythonlings.core.exercise import Exercise
from pythonlings.core.runner import run

ROOT = Path(__file__).resolve().parent.parent.parent
CHECK_SRC = (ROOT / "checks" / "type_hints" / "type_hints1.py").read_text(
    encoding="utf-8"
)


def _run_case(tmp_path: Path, exercise_src: str) -> object:
    ex_path = tmp_path / "ex.py"
    check_path = tmp_path / "check.py"
    ex_path.write_text(exercise_src, encoding="utf-8")
    check_path.write_text(CHECK_SRC, encoding="utf-8")
    exercise = Exercise(
        name="type_hints1",
        path=ex_path,
        check_path=check_path,
        topic="type_hints",
        hint="",
    )
    return run(exercise)


def test_correct_annotation_passes(tmp_path: Path) -> None:
    result = _run_case(tmp_path, "count: int = 0\n")
    assert result.passed is True
    assert "type_hints1 ✓" in result.stdout


def test_wrong_type_fails_with_clear_message(tmp_path: Path) -> None:
    result = _run_case(tmp_path, "count: str = ''\n")
    assert result.passed is False
    assert "AssertionError" in result.stderr
    assert "count should be annotated as int" in result.stderr
    assert "NameError" not in result.stderr


def test_missing_annotation_fails_with_clear_message(tmp_path: Path) -> None:
    result = _run_case(tmp_path, "total = 0\n")
    assert result.passed is False
    assert "AssertionError" in result.stderr
    assert "count should be annotated as int" in result.stderr
    assert "NameError" not in result.stderr


def test_none_annotation_hook_fails_with_clear_message(tmp_path: Path) -> None:
    result = _run_case(tmp_path, "__annotate__ = None\n")
    assert result.passed is False
    assert "AssertionError" in result.stderr
    assert "count should be annotated as int" in result.stderr
    assert "TypeError" not in result.stderr


def test_callable_annotation_hook_passes(tmp_path: Path) -> None:
    exercise_src = "def __annotate__(format_value):\n    return {'count': int}\n"
    result = _run_case(tmp_path, exercise_src)
    assert result.passed is True
    assert "type_hints1 ✓" in result.stdout
