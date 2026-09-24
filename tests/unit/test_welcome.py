from __future__ import annotations

from pythonlings.screens.welcome import welcome_text


def test_welcome_text_explains_the_loop() -> None:
    text = welcome_text()

    assert "I AM NOT DONE" in text
    # v0.4.0 reruns checks as you type in the built-in editor — no manual save,
    # so the copy must not tell users to "save".
    assert "as you type" in text.lower()
    assert "save" not in text.lower()
    assert "F1" in text
