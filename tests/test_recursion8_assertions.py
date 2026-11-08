import ast
import pathlib


CHECK_PATH = pathlib.Path(__file__).resolve().parents[1] / "checks" / "recursion" / "recursion8.py"


def _assertion_messages():
    tree = ast.parse(CHECK_PATH.read_text())
    messages = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            messages.append(node.msg)
    return messages


def test_recursion8_assertions_have_actionable_messages():
    messages = _assertion_messages()
    assert messages, "recursion8.py should contain assertions"
    for msg in messages:
        assert msg is not None, "every assertion in recursion8.py must include a message"
        assert isinstance(msg, ast.JoinedStr), (
            "assertion messages should be f-strings describing expected vs actual values"
        )
