# tests/test_json_checks_messages.py
import ast
from dataclasses import replace
from pathlib import Path

import pytest

from pythonlings.core.manifest import load
from pythonlings.core.runner import run_verify

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ROOT / "checks" / "json" / f"json{number}.py" for number in range(1, 7)
]


def test_check_lines_within_80_chars() -> None:
    for path in CHECKS:
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            assert len(line) <= 80, f"{path}:{lineno} exceeds 80 chars"


def test_asserts_have_messages() -> None:
    for path in CHECKS:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                assert node.msg is not None, (
                    f"{path}:{node.lineno} assert lacks a message"
                )


@pytest.mark.parametrize(
    ("name", "source", "expected"),
    [
        (
            "json1",
            "data = {}\nname = 'Ada'\n",
            "{'name': 'Ada', 'language': 'Python'}",
        ),
        ("json2", "text = '{}'\n", '\'{"a": 1, "b": 2}\''),
    ],
)
def test_failure_reports_expected_json_value(
    tmp_path: Path, name: str, source: str, expected: str
) -> None:
    path = tmp_path / "wrong.py"
    path.write_text(source, encoding="utf-8")
    exercise = replace(load(ROOT).by_name(name), path=path)

    result = run_verify(exercise)

    assert not result.passed
    assert "AssertionError" in result.stderr
    assert expected in result.stderr.splitlines()[-1]
