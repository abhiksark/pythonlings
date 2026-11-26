import ast
from pathlib import Path


CHECKS_DIR = Path(__file__).resolve().parent.parent / "checks" / "dataclasses"


def _asserts_without_messages(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assert) and node.msg is None
    ]


def test_dataclasses1_asserts_have_messages():
    path = CHECKS_DIR / "dataclasses1.py"
    assert _asserts_without_messages(path) == []


def test_dataclasses2_asserts_have_messages():
    path = CHECKS_DIR / "dataclasses2.py"
    assert _asserts_without_messages(path) == []


def test_dataclasses_checks_wrap_at_80_chars():
    for name in ("dataclasses1.py", "dataclasses2.py"):
        path = CHECKS_DIR / name
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            assert len(line) <= 80, f"{name}:{lineno} exceeds 80 chars: {line!r}"
