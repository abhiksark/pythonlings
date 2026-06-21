from __future__ import annotations

from pythonlings.screens.welcome import welcome_text


def test_welcome_text_explains_the_loop() -> None:
    text = welcome_text()

    assert "I AM NOT DONE" in text
    assert "save" in text.lower()
    assert "F1" in text
