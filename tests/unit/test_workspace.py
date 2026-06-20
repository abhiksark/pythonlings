from __future__ import annotations

from pathlib import Path

from pythonlings.core.workspace import default_workspace_root, is_workspace


def test_default_root_uses_env_when_set(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTHONLINGS_HOME", str(tmp_path / "custom"))
    assert default_workspace_root() == (tmp_path / "custom").resolve()


def test_default_root_falls_back_to_hidden_home_dir(monkeypatch):
    monkeypatch.delenv("PYTHONLINGS_HOME", raising=False)
    assert default_workspace_root() == (Path.home() / ".pythonlings").resolve()


def test_is_workspace_true_only_with_info_toml(tmp_path):
    assert is_workspace(tmp_path) is False
    (tmp_path / "info.toml").write_text("", encoding="utf-8")
    assert is_workspace(tmp_path) is True
