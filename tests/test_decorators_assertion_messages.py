import ast
from pathlib import Path


CHECKS = Path(__file__).resolve().parent.parent / "checks" / "decorators"


def _asserts_without_msg(path):
    tree = ast.parse(path.read_text())
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert) and node.msg is None:
            missing.append(node.lineno)
    return missing


def test_decorators2_asserts_have_messages():
    assert _asserts_without_msg(CHECKS / "decorators2.py") == []


def test_decorators5_asserts_have_messages():
    assert _asserts_without_msg(CHECKS / "decorators5.py") == []
