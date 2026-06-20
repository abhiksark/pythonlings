from __future__ import annotations

import os
from pathlib import Path


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
