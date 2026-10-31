import ast
from pathlib import Path


CHECKS = [
    Path("checks/json/json1.py"),
    Path("checks/json/json2.py"),
    Path("checks/json/json3.py"),
]


def test_check_lines_within_80_chars():
    for path in CHECKS:
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            assert len(line) <= 80, f"{path}:{lineno} exceeds 80 chars"


def test_asserts_have_messages():
    for path in CHECKS:
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                assert node.msg is not None, (
                    f"{path}:{node.lineno} assert lacks a message"
                )
