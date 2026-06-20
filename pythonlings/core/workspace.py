from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from pythonlings.core.curriculum import init_workspace


@dataclass(frozen=True)
class ResolvedWorkspace:
    root: Path
    created: bool


def default_workspace_root() -> Path:
    """Where a no-argument `pythonlings` keeps its workspace.

    `PYTHONLINGS_HOME` overrides; otherwise a hidden `~/.pythonlings`.
    """
    env = os.environ.get("PYTHONLINGS_HOME")
    if env:
        return Path(env).expanduser().resolve()
    return (Path.home() / ".pythonlings").resolve()


def is_workspace(path: Path) -> bool:
    """True if `path` is a pythonlings workspace (has an `info.toml`)."""
    return (path / "info.toml").is_file()


def resolve_workspace_root(
    cwd: Path,
    explicit_root: Path | None = None,
    *,
    create_if_missing: bool = False,
) -> ResolvedWorkspace:
    """Pick the workspace root for a command.

    Order: an explicit `--root`, then the current directory if it is a
    workspace, then the default home workspace, then (only when
    `create_if_missing`) a freshly created home workspace.
    """
    if explicit_root is not None:
        return ResolvedWorkspace(explicit_root.expanduser().resolve(), created=False)

    cwd = cwd.resolve()
    if is_workspace(cwd):
        return ResolvedWorkspace(cwd, created=False)

    home = default_workspace_root()
    if is_workspace(home):
        return ResolvedWorkspace(home, created=False)

    if create_if_missing:
        return ResolvedWorkspace(init_workspace(home), created=True)
    return ResolvedWorkspace(home, created=False)
