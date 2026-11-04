# tests/test_functional_assertion_messages.py
import ast
from pathlib import Path


CHECKS_DIR = Path(__file__).resolve().parent.parent / "checks" / "functional"

BATCH = ("functional7.py", "functional8.py", "functional9.py")


def _asserts_without_message(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert) and node.msg is None:
            missing.append(node.lineno)
    return missing


def test_functional7_asserts_have_messages():
    path = CHECKS_DIR / "functional7.py"
    assert _asserts_without_message(path) == []


def test_functional8_asserts_have_messages():
    path = CHECKS_DIR / "functional8.py"
    assert _asserts_without_message(path) == []


def test_functional9_asserts_have_messages():
    path = CHECKS_DIR / "functional9.py"
    assert _asserts_without_message(path) == []


def test_batch_lines_fit_eighty_columns():
    too_long = [
        f"{name}:{number} ({len(line)} columns)"
        for name in BATCH
        for number, line in enumerate(
            (CHECKS_DIR / name).read_text(encoding="utf-8").splitlines(), 1
        )
        if len(line) > 80
    ]
    assert too_long == []
