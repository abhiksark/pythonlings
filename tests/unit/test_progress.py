from __future__ import annotations

from pythonlings.core.state import completed_count
from pythonlings.widgets.progress import format_progress


def test_format_progress_shows_topic_and_overall() -> None:
    line = format_progress(2, 5, 10, 100)

    assert "2/5" in line
    assert "40%" in line  # topic 2/5
    assert "10/100" in line
    assert "10%" in line  # overall 10/100
    assert "Overall" in line


def test_format_progress_handles_zero_totals() -> None:
    line = format_progress(0, 0, 0, 0)

    assert "0/0" in line
    assert "0%" in line


def test_completed_count_ignores_names_not_in_curriculum() -> None:
    # Stale state (renamed/removed exercises) must not inflate the count.
    assert completed_count(["a", "b", "c"], {"a", "b", "ghost"}) == 2


def test_completed_count_empty() -> None:
    assert completed_count([], set()) == 0
