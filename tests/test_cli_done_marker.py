from __future__ import annotations

from pathlib import Path

from pythonlings.core.exercise import Exercise


def test_run_message_references_done_marker(tmp_path: Path, monkeypatch, capsys):
    """The CLI's pending-marker message must track Exercise.DONE_MARKER."""
    from pythonlings import cli

    exercise_path = tmp_path / "exercise.py"
    exercise_path.write_text(
        f"{Exercise.DONE_MARKER}\nprint('hi')\n", encoding="utf-8"
    )
    check_path = tmp_path / "check.py"
    check_path.write_text("", encoding="utf-8")

    ex = Exercise(
        name="demo",
        path=exercise_path,
        check_path=check_path,
        topic="basics",
        hint="",
    )

    class FakeManifest:
        def by_name(self, name: str) -> Exercise:
            assert name == "demo"
            return ex

    class FakeResult:
        stdout = ""
        stderr = ""
        timed_out = False
        exit_code = 0
        duration_s = 0.0

    monkeypatch.setattr(
        "pythonlings.core.manifest.load", lambda root: FakeManifest()
    )
    monkeypatch.setattr(
        "pythonlings.core.runner.run", lambda exercise: FakeResult()
    )

    exit_code = cli._cmd_run(tmp_path, "demo")
    captured = capsys.readouterr()

    assert exit_code == 1
    assert Exercise.DONE_MARKER in captured.err
