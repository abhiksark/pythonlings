from __future__ import annotations

from pathlib import Path

from pythonlings.core.workspace import (
    ResolvedWorkspace,
    default_workspace_root,
    is_workspace,
    resolve_workspace_root,
)


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


def _make_ws(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    (path / "info.toml").write_text("", encoding="utf-8")
    return path


def test_resolve_prefers_explicit_root(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTHONLINGS_HOME", str(tmp_path / "home"))
    explicit = tmp_path / "given"
    out = resolve_workspace_root(tmp_path / "cwd", explicit, create_if_missing=True)
    assert out == ResolvedWorkspace(explicit.resolve(), created=False)


def test_resolve_uses_cwd_when_cwd_is_workspace(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTHONLINGS_HOME", str(tmp_path / "home"))
    cwd = _make_ws(tmp_path / "cwd")
    out = resolve_workspace_root(cwd, None, create_if_missing=True)
    assert out == ResolvedWorkspace(cwd.resolve(), created=False)


def test_resolve_resumes_existing_home_workspace(tmp_path, monkeypatch):
    home = _make_ws(tmp_path / "home")
    monkeypatch.setenv("PYTHONLINGS_HOME", str(home))
    out = resolve_workspace_root(tmp_path / "cwd", None, create_if_missing=True)
    assert out == ResolvedWorkspace(home.resolve(), created=False)


def test_resolve_creates_home_when_missing(tmp_path, monkeypatch):
    home = tmp_path / "home"
    monkeypatch.setenv("PYTHONLINGS_HOME", str(home))
    out = resolve_workspace_root(tmp_path / "cwd", None, create_if_missing=True)
    assert out.root == home.resolve()
    assert out.created is True
    assert (home / "info.toml").is_file()


def test_resolve_does_not_create_when_flag_off(tmp_path, monkeypatch):
    home = tmp_path / "home"
    monkeypatch.setenv("PYTHONLINGS_HOME", str(home))
    out = resolve_workspace_root(tmp_path / "cwd", None, create_if_missing=False)
    assert out == ResolvedWorkspace(home.resolve(), created=False)
    assert not home.exists()
