# tests/tui/test_app_pilot.py
import asyncio
import shutil
import threading
import webbrowser
from pathlib import Path

import pytest
from textual.widgets import Footer, Markdown, Static, TextArea
from textual.worker import WorkerCancelled

from pythonlings.app import PythonlingsApp
from pythonlings.core.exercise import RunResult
from pythonlings.core.state import State
from pythonlings.core.state import save as save_state
from pythonlings.screens import track as track_module
from pythonlings.screens.docs import DocsScreen
from pythonlings.screens.topic_picker import TopicPickerScreen
from pythonlings.screens.track import _AUTO_ADVANCE_SECONDS, TrackScreen
from pythonlings.widgets.output_panel import OutputPanel

MULTI = Path(__file__).parent.parent / "fixtures" / "multi_topic"


def _work_copy(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    shutil.copytree(MULTI, work, ignore=shutil.ignore_patterns(".pythonlings"))
    # These tests exercise the returning-user flow, so start past the
    # first-launch welcome overlay (covered in test_welcome_pilot.py).
    save_state(work, State(seen_intro=True))
    return work


async def _settle(pilot) -> None:
    for _ in range(6):
        try:
            await pilot.app.workers.wait_for_complete()
        except WorkerCancelled:
            pass
        await pilot.pause()


@pytest.mark.asyncio
async def test_default_launch_opens_first_pending_exercise(
    tmp_path: Path,
) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a1"


@pytest.mark.asyncio
async def test_invalid_utf8_exercise_stays_open_without_overwriting(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    exercise_path = work / "exercises" / "alpha" / "a1.py"
    exercise_path.write_bytes(b"\xff")
    app = PythonlingsApp(root=work)

    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.current == "a1"
        rendered = app.screen.query_one(OutputPanel).renderable_text()
        assert "UTF-8" in rendered
        assert "a1" in rendered
        assert str(exercise_path) in rendered
        assert "a1" not in app.state.completed
        assert app.screen.query_one("#code", TextArea).read_only
        await pilot.press("x")
        await pilot.pause(0.8)
        await pilot.press("ctrl+q")

    assert exercise_path.read_bytes() == b"\xff"


@pytest.mark.asyncio
async def test_advance_to_invalid_utf8_exercise_preserves_its_bytes(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    (work / "exercises" / "alpha" / "a1.py").write_text(
        "x = 1\n", encoding="utf-8"
    )
    exercise_path = work / "exercises" / "alpha" / "a2.py"
    exercise_path.write_bytes(b"\xff")
    app = PythonlingsApp(root=work)

    async with app.run_test() as pilot:
        await _settle(pilot)
        assert app.screen.current == "a2"
        assert app.screen.query_one("#code", TextArea).text == ""
        assert "UTF-8" in app.screen.query_one(OutputPanel).renderable_text()
        await pilot.pause(0.8)
        await pilot.press("f4")

    assert exercise_path.read_bytes() == b"\xff"


@pytest.mark.asyncio
async def test_picker_lists_topics_with_progress(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        rendered = " ".join(
            str(row.content) for row in app.screen.query(".topic-row").results()
        )
        assert "alpha" in rendered
        assert "beta" in rendered


@pytest.mark.asyncio
async def test_enter_on_picker_opens_selected_topic(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)
        await pilot.press("enter")
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a1"


@pytest.mark.asyncio
async def test_picker_shows_first_run_start_banner(tmp_path: Path) -> None:
    # Needs genuine first-run state (no seen_intro seed) for the banner.
    work = tmp_path / "work"
    shutil.copytree(MULTI, work, ignore=shutil.ignore_patterns(".pythonlings"))
    app = PythonlingsApp(root=work, force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        banner = str(app.screen.query_one("#topic-banner").content)
        assert "Start here" in banner
        assert "alpha" in banner


@pytest.mark.asyncio
async def test_picker_rows_show_status_labels(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(
        work, State(completed={"a1"}, seen_intro=True, last_topic="alpha")
    )
    app = PythonlingsApp(root=work, force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        rendered = " ".join(
            str(row.content) for row in app.screen.query(".topic-row").results()
        )
        assert "Continue" in rendered
        assert "Start" in rendered


@pytest.mark.asyncio
async def test_start_topic_opens_track(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"


@pytest.mark.asyncio
async def test_default_launch_resumes_last_incomplete_exercise(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    save_state(
        work,
        State(seen_intro=True, last_topic="alpha", last_exercise="a2"),
    )
    app = PythonlingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a2"


@pytest.mark.asyncio
async def test_default_launch_falls_back_from_invalid_resume_state(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    save_state(
        work,
        State(seen_intro=True, last_topic="missing", last_exercise="ghost"),
    )
    app = PythonlingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a1"


@pytest.mark.asyncio
async def test_force_picker_launch_ignores_resume_state(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(
        work,
        State(seen_intro=True, last_topic="alpha", last_exercise="a2"),
    )
    app = PythonlingsApp(root=work, force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_f4_returns_to_picker(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        await pilot.press("f4")
        await pilot.pause()
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_narrow_layout_keeps_navigation_discoverable_and_usable(
    tmp_path: Path,
) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test(size=(40, 15)) as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)

        footer = app.screen.query_one(Footer)
        keys = {key.key: key for key in footer.query("FooterKey")}
        assert "ctrl+p" not in keys
        for key_name in ("f4", "f5", "escape"):
            key = keys[key_name]
            assert key.region.x >= footer.region.x
            assert key.region.right <= footer.region.right

        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)
        docs_footer = str(app.screen.query_one("#docs-footer", Static).content)
        assert docs_footer.startswith("Esc Close")

        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, TrackScreen)

        await pilot.press("f4")
        await pilot.pause()
        assert isinstance(app.screen, TopicPickerScreen)
        picker_footer = app.screen.query_one(Footer)
        picker_keys = {key.key: key for key in picker_footer.query("FooterKey")}
        escape_key = picker_keys["escape"]
        assert escape_key.region.x >= picker_footer.region.x
        assert escape_key.region.right <= picker_footer.region.right

        await pilot.press("escape")
        await pilot.pause()
        assert app.return_code == 0


@pytest.mark.asyncio
async def test_normal_width_footer_keeps_all_track_labels(
    tmp_path: Path,
) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test(size=(80, 24)) as pilot:
        await _settle(pilot)
        footer = app.screen.query_one(Footer)
        footer_keys = list(footer.query("FooterKey"))
        keys = {key.key: key for key in footer_keys}
        assert [
            key.key
            for key in footer_keys
            if key.key in {"f1", "f2", "f3", "f4", "f5", "escape"}
        ] == ["f1", "f2", "f3", "f4", "f5", "escape"]
        assert keys["ctrl+p"].description == "palette"
        assert {
            key_name: keys[key_name].description
            for key_name in ("f1", "f2", "f3", "f4", "f5", "escape")
        } == {
            "f1": "Hint",
            "f2": "Reset",
            "f3": "List",
            "f4": "Topics",
            "f5": "Docs",
            "escape": "Quit",
        }
        assert all(
            key.region.right <= footer.region.right for key in keys.values()
        )


@pytest.mark.asyncio
async def test_docs_footer_uses_its_laid_out_width_at_41_columns(
    tmp_path: Path,
) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test(size=(41, 15)) as pilot:
        await _settle(pilot)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)

        docs_footer = app.screen.query_one("#docs-footer", Static)
        footer_text = str(docs_footer.content)
        assert docs_footer.size.width == 23
        assert footer_text == "Esc Close | O Docs"
        assert len(footer_text) <= docs_footer.size.width


@pytest.mark.asyncio
async def test_escape_quits_from_track_screen(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        await pilot.press("escape")
        await pilot.pause()
        assert app.return_code == 0


@pytest.mark.asyncio
async def test_escape_quits_from_topic_picker(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)
        await pilot.press("escape")
        await pilot.pause()
        assert app.return_code == 0


@pytest.mark.asyncio
async def test_f5_opens_docs_popup_for_current_exercise(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)
        assert "a1" in str(app.screen.query_one("#docs-title", Static).content)
        rendered = app.screen.query_one("#docs-content", Markdown)._markdown
        assert "Local reference" in rendered
        assert "# Variables" not in rendered
        assert "Assigning names" in rendered
        assert (
            "https://docs.python.org/3/tutorial/introduction.html" in rendered
        )
        footer = app.screen.query_one("#docs-footer", Static).content
        assert "O Open official docs" in str(footer)
        assert "Esc Close" in str(footer)


@pytest.mark.asyncio
async def test_escape_closes_docs_popup_without_quitting(
    tmp_path: Path,
) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, TrackScreen)
        assert app.return_code is None


@pytest.mark.asyncio
async def test_docs_popup_can_open_browser(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    opened: list[str] = []
    monkeypatch.setattr(webbrowser, "open", lambda url: opened.append(url))
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)
        await pilot.press("o")
        await pilot.pause()
        assert opened == [
            "https://docs.python.org/3/tutorial/introduction.html"
        ]


@pytest.mark.asyncio
async def test_track_records_resume_when_loaded(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert app.state.seen_intro is True
        assert app.state.last_topic == "alpha"
        assert app.state.last_exercise == "a1"


@pytest.mark.asyncio
async def test_instant_advance_updates_resume_to_next_exercise(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "x = 1\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "a1" in app.state.completed
        assert track.current == "a2"
        assert app.state.last_topic == "alpha"
        assert app.state.last_exercise == "a2"


@pytest.mark.asyncio
async def test_marker_pass_schedules_auto_advance(tmp_path: Path) -> None:
    """Checks passing with the marker still present starts the countdown."""
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "# I AM NOT DONE\nx = 1\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "a1" not in app.state.completed
        assert track.current == "a1"
        assert track._advance_timer is not None
        assert (
            f"advancing to the next exercise in {_AUTO_ADVANCE_SECONDS}s"
            in track.query_one(OutputPanel).renderable_text().lower()
        )


@pytest.mark.asyncio
async def test_auto_advance_countdown_ticks_down_each_second(
    tmp_path: Path,
) -> None:
    """Each tick decrements the countdown and updates the panel text."""
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "# I AM NOT DONE\nx = 1\n"
        track._flush_and_run()
        await _settle(pilot)
        assert track._advance_remaining == _AUTO_ADVANCE_SECONDS

        track._tick_advance()
        await pilot.pause()
        assert track._advance_remaining == _AUTO_ADVANCE_SECONDS - 1
        assert (
            f"advancing to the next exercise in {_AUTO_ADVANCE_SECONDS - 1}s"
            in track.query_one(OutputPanel).renderable_text().lower()
        )

        for _ in range(_AUTO_ADVANCE_SECONDS - 2):
            track._tick_advance()
        await pilot.pause()
        assert track._advance_remaining == 1
        assert "a1" not in app.state.completed

        track._tick_advance()  # remaining hits 0: fires the auto-advance
        await _settle(pilot)
        assert "a1" in app.state.completed
        assert track.current == "a2"


@pytest.mark.asyncio
async def test_auto_advance_fires_strips_marker_and_advances(
    tmp_path: Path,
) -> None:
    """When the countdown fires, the marker is stripped on disk and advances."""
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        checked_text = "# I AM NOT DONE\nx = 1\n"
        track.query_one("#code", TextArea).text = checked_text
        track._flush_and_run()
        await _settle(pilot)
        # Simulate the auto-advance timer firing rather than waiting on it.
        track._auto_advance(track._exercise("a1"), checked_text)
        await _settle(pilot)
        assert "a1" in app.state.completed
        assert track.current == "a2"
        assert "# I AM NOT DONE" not in (
            work / "exercises" / "alpha" / "a1.py"
        ).read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_editing_during_countdown_cancels_auto_advance(
    tmp_path: Path,
) -> None:
    """Resuming an edit mid-countdown cancels the auto-advance timer."""
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "# I AM NOT DONE\nx = 1\n"
        track._flush_and_run()
        await _settle(pilot)
        assert track._advance_timer is not None
        track.query_one("#code", TextArea).text = "# I AM NOT DONE\nx = 2\n"
        await _settle(pilot)
        assert track._advance_timer is None
        assert "a1" not in app.state.completed
        assert track.current == "a1"


@pytest.mark.asyncio
async def test_failed_run_shows_progressive_nudge(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "x = 99\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "alpha one" in track.query_one(OutputPanel).renderable_text()


@pytest.mark.asyncio
async def test_inflight_pass_does_not_check_new_editor_text(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    started, release = threading.Event(), threading.Event()

    def delayed_pass(exercise):
        started.set()
        assert release.wait(timeout=5)
        return RunResult(False, 0, "ok", "", 0.1, False)

    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        editor = track.query_one("#code", TextArea)
        monkeypatch.setattr(track_module, "run_exercise", delayed_pass)
        monkeypatch.setattr(track_module, "_DEBOUNCE_SECONDS", 60)
        editor.text = "# I AM NOT DONE\nx = 1\n"
        track._flush_and_run()
        try:
            assert await asyncio.to_thread(started.wait, 5)
            editor.text = "# I AM NOT DONE\nx = 99\n"
            await pilot.pause()
        finally:
            release.set()
        await _settle(pilot)
        assert track._advance_timer is None
        assert track.current == "a1"
        assert "a1" not in app.state.completed


@pytest.mark.asyncio
async def test_marker_in_string_does_not_start_countdown(
    tmp_path: Path,
) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        text = 'message = """\n# I AM NOT DONE\n"""\nx = 1\n'
        track.query_one("#code", TextArea).text = text
        track._flush_and_run()
        await _settle(pilot)
        assert track._advance_timer is None
        assert track._exercise("a1").path.read_text(encoding="utf-8") == text
        assert (
            "remove" in track.query_one(OutputPanel).renderable_text().lower()
        )


@pytest.mark.asyncio
async def test_cancelled_old_pass_cannot_replace_a_newer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    started, release = threading.Event(), threading.Event()

    def controlled_run(exercise):
        if exercise.path.read_text(encoding="utf-8").endswith("x = 1\n"):
            started.set()
            assert release.wait(timeout=5)
            return RunResult(False, 0, "ok", "", 0.1, False)
        return RunResult(False, 1, "", "expected x = 1", 0.1, False)

    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        editor = track.query_one("#code", TextArea)
        monkeypatch.setattr(track_module, "run_exercise", controlled_run)
        monkeypatch.setattr(track_module, "_DEBOUNCE_SECONDS", 60)
        checked = "# I AM NOT DONE\nx = 1\n"
        editor.text = checked
        track._flush_and_run()
        try:
            assert await asyncio.to_thread(started.wait, 5)
            editor.text = "# I AM NOT DONE\nx = 99\n"
            track._flush_and_run()
            await _settle(pilot)
            assert "expected x = 1" in (
                track.query_one(OutputPanel).renderable_text()
            )
            editor.text = checked
            await pilot.pause()
        finally:
            release.set()
        await _settle(pilot)
        assert track._advance_timer is None
        assert track.current == "a1"
        assert "a1" not in app.state.completed


@pytest.mark.asyncio
@pytest.mark.parametrize("leave_key", ["f4", "escape", "ctrl+q"])
async def test_revert_to_loaded_text_is_persisted_when_leaving(
    tmp_path: Path, leave_key: str
) -> None:
    work = _work_copy(tmp_path)
    exercise_path = work / "exercises" / "alpha" / "a1.py"
    original_text = exercise_path.read_text(encoding="utf-8")
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        editor = track.query_one("#code", TextArea)

        editor.text = "x = 99\n"
        await pilot.pause(0.7)
        await _settle(pilot)
        assert exercise_path.read_text(encoding="utf-8") == "x = 99\n"

        editor.text = original_text
        await pilot.pause()
        await pilot.press(leave_key)
        await pilot.pause()

        assert editor.text == original_text
        assert exercise_path.read_text(encoding="utf-8") == original_text
        if leave_key == "f4":
            assert isinstance(app.screen, TopicPickerScreen)
        else:
            assert app.return_code == 0


@pytest.mark.asyncio
async def test_revert_is_persisted_when_quitting_from_docs(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    exercise_path = work / "exercises" / "alpha" / "a1.py"
    original_text = exercise_path.read_text(encoding="utf-8")
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        editor = track.query_one("#code", TextArea)

        editor.text = "x = 99\n"
        await pilot.pause(0.7)
        await _settle(pilot)
        editor.text = original_text
        await pilot.pause()

        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)
        await pilot.press("ctrl+q")
        await pilot.pause()

        assert exercise_path.read_text(encoding="utf-8") == original_text
        assert app.return_code == 0


@pytest.mark.asyncio
async def test_revert_and_rapid_edits_use_debounced_persistence(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    exercise_path = work / "exercises" / "alpha" / "a1.py"
    original_text = exercise_path.read_text(encoding="utf-8")
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        editor = track.query_one("#code", TextArea)

        editor.text = "x = 1\n"
        editor.text = "x = 2\n"
        await pilot.pause(0.7)
        await _settle(pilot)
        assert exercise_path.read_text(encoding="utf-8") == "x = 2\n"

        editor.text = original_text
        await pilot.pause(0.7)
        await _settle(pilot)
        assert exercise_path.read_text(encoding="utf-8") == original_text


@pytest.mark.asyncio
async def test_initial_load_does_not_schedule_a_save(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    flushes: list[object] = []
    original_flush = TrackScreen._flush_and_run

    def record_flush(screen: TrackScreen) -> None:
        flushes.append(screen.current)
        original_flush(screen)

    monkeypatch.setattr(TrackScreen, "_flush_and_run", record_flush)
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await pilot.pause(0.7)
        await _settle(pilot)

    assert flushes == []


@pytest.mark.asyncio
async def test_hint_visibility_resets_after_advance(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.action_toggle_hint()
        await pilot.pause()
        assert "visible" in track.query_one("#hint").classes

        track.query_one("#code", TextArea).text = "x = 1\n"
        track._flush_and_run()
        await _settle(pilot)
        assert track.current == "a2"
        assert "visible" not in track.query_one("#hint").classes


@pytest.mark.asyncio
async def test_solving_a_topic_marks_progress(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="beta")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        # beta has one exercise, b1; solve it.
        track.query_one("#code", TextArea).text = "z = 3\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "b1" in app.state.completed


@pytest.mark.asyncio
async def test_picker_refreshes_progress_after_returning(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="beta")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "z = 3\n"
        track._flush_and_run()
        await _settle(pilot)
        await pilot.press("f4")
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)
        rendered = " ".join(
            str(row.content) for row in app.screen.query(".topic-row").results()
        )
        # beta's one exercise is now done -> "1/1" must appear.
        assert "1/1" in rendered
