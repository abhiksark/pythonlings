from __future__ import annotations

from pathlib import Path

import pythonlings.app as app_module
from pythonlings.cli import main


def test_bare_run_creates_home_workspace_and_launches(tmp_path, monkeypatch, capsys):
    home = tmp_path / "home"
    monkeypatch.setenv("PYTHONLINGS_HOME", str(home))
    monkeypatch.chdir(tmp_path)  # cwd is not a workspace

    calls = {}

    def fake_run_tui(root, start_topic, force_picker=False):
        calls["root"] = root
        return 0

    monkeypatch.setattr(app_module, "run_tui", fake_run_tui)

    code = main([])

    assert code == 0
    assert (home / "info.toml").is_file()
    assert calls["root"] == home.resolve()
    assert "Created your workspace at" in capsys.readouterr().out


def test_bare_run_resumes_existing_home_without_notice(tmp_path, monkeypatch, capsys):
    home = tmp_path / "home"
    monkeypatch.setenv("PYTHONLINGS_HOME", str(home))
    main(["init", "--path", str(home)])
    capsys.readouterr()
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(app_module, "run_tui", lambda root, t, force_picker=False: 0)

    code = main([])

    assert code == 0
    assert "Created your workspace" not in capsys.readouterr().out


def test_init_with_no_path_targets_home(tmp_path, monkeypatch, capsys):
    home = tmp_path / "home"
    monkeypatch.setenv("PYTHONLINGS_HOME", str(home))
    monkeypatch.chdir(tmp_path)

    code = main(["init"])

    assert code == 0
    assert (home / "info.toml").is_file()
