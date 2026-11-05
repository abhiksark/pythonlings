# tests/unit/test_check_namespaces.py
from pathlib import Path

import pytest

from solutions._answers import ANSWERS


def test_area_check_preserves_learner_globals() -> None:
    namespace = {"__name__": "__main__"}
    exec(ANSWERS["oop_advanced3"], namespace)
    namespace["area"] = 0
    check = (
        Path(__file__).resolve().parents[2]
        / "checks" / "oop_advanced" / "oop_advanced3.py"
    )

    exec(
        compile(check.read_text(encoding="utf-8"), str(check), "exec"),
        namespace,
    )

    assert namespace["area"] == 0


@pytest.mark.parametrize(
    ("name", "function", "argument"),
    [
        ("functional1", "square", 0),
        ("functional2", "absolute", 0),
        ("functional2", "absolute", -100),
        ("functional6", "apply_twice", 0),
    ],
)
def test_functional_messages_do_not_repeat_failed_calls(
    name: str, function: str, argument: int
) -> None:
    namespace = {"__name__": "__main__"}
    exec(ANSWERS[name], namespace)
    original = namespace[function]
    calls = []

    def wrong_once(*args):
        if args[-1] != argument:
            return original(*args)
        calls.append(args)
        if len(calls) > 1:
            raise RuntimeError("Failure message called learner code again")
        return -1

    namespace[function] = wrong_once
    check = (
        Path(__file__).resolve().parents[2]
        / "checks" / "functional" / f"{name}.py"
    )
    with pytest.raises(AssertionError, match="should be"):
        exec(
            compile(check.read_text(encoding="utf-8"), str(check), "exec"),
            namespace,
        )
    assert len(calls) == 1
