# tests/test_datetime_assertion_messages.py
import ast
from pathlib import Path

CHECKS = Path(__file__).resolve().parent.parent / "checks" / "datetime"


def test_datetime_checks_lines_within_limit() -> None:
    for number in range(1, 7):
        name = f"datetime{number}.py"
        path = CHECKS / name
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            assert len(line) <= 80, f"{name}:{lineno} exceeds 80 chars"


def test_datetime_checks_assertions_have_messages() -> None:
    for number in range(1, 7):
        name = f"datetime{number}.py"
        path = CHECKS / name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                assert node.msg is not None, (
                    f"{name}:{node.lineno} assert lacks message"
                )
