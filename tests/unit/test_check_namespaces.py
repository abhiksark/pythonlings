# tests/unit/test_check_namespaces.py
from pathlib import Path

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
