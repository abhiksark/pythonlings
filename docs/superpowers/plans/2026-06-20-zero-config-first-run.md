# Zero-config First Run Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make bare `pythonlings` set up a workspace automatically (hidden `~/.pythonlings`, overridable) and launch the first exercise, so a new user just types `pythonlings`.

**Architecture:** A new `core/workspace.py` owns the default location and a precedence resolver (explicit `--root` → cwd-workspace → home-workspace → create home). `cli.py` switches `--root`/`--path` to lazy defaults and routes every command's root through the resolver; only TUI-launch commands auto-create. `init` gets friendlier, actionable messages. No curriculum, state-format, or TUI changes.

**Tech Stack:** Python 3.9+, argparse, pathlib, dataclasses, pytest (+ pytest-asyncio auto mode). Textual stays out of unit tests via mocking `run_tui`.

## Global Constraints

- `requires-python = ">=3.9"`; start every new module with `from __future__ import annotations`.
- Default workspace root: `PYTHONLINGS_HOME` env var if set, else `~/.pythonlings`.
- The unrelated `pylings` PyPI name is never used; command/package are `pythonlings`.
- Conventional commit prefixes (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- CLI tests must mock `pythonlings.app.run_tui` — never launch Textual.
- Target release: **0.4.0** (minor).
- Keep core free of UI imports (`core/` has no Textual/screens imports).

---

### Task 1: Default location + workspace detection (`core/workspace.py`)

**Files:**
- Create: `pythonlings/core/workspace.py`
- Test: `tests/unit/test_workspace.py`

**Interfaces:**
- Produces: `default_workspace_root() -> Path` (reads `PYTHONLINGS_HOME`, else `~/.pythonlings`, always expanded+resolved); `is_workspace(path: Path) -> bool` (True iff `path/"info.toml"` is a file).

- [ ] **Step 1: Write the failing tests**

```python
# tests/unit/test_workspace.py
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/unit/test_workspace.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'pythonlings.core.workspace'`.

- [ ] **Step 3: Write minimal implementation**

```python
# pythonlings/core/workspace.py
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/unit/test_workspace.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add pythonlings/core/workspace.py tests/unit/test_workspace.py
git commit -m "feat: add default_workspace_root and is_workspace helpers"
```

---

### Task 2: Workspace resolver (`resolve_workspace_root`)

**Files:**
- Modify: `pythonlings/core/workspace.py`
- Test: `tests/unit/test_workspace.py`

**Interfaces:**
- Consumes: `default_workspace_root`, `is_workspace` (Task 1); `init_workspace` from `pythonlings.core.curriculum` (signature `init_workspace(path: Path, *, force: bool = False) -> Path`).
- Produces: `ResolvedWorkspace` (frozen dataclass with `root: Path`, `created: bool`); `resolve_workspace_root(cwd: Path, explicit_root: Path | None = None, *, create_if_missing: bool = False) -> ResolvedWorkspace`.

Precedence: explicit_root → cwd-is-workspace → home-is-workspace → (create home if `create_if_missing` else return home uncreated).

- [ ] **Step 1: Write the failing tests**

```python
# append to tests/unit/test_workspace.py
from pythonlings.core.workspace import ResolvedWorkspace, resolve_workspace_root


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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/unit/test_workspace.py -q`
Expected: FAIL with `ImportError: cannot import name 'resolve_workspace_root'`.

- [ ] **Step 3: Write minimal implementation**

```python
# add to pythonlings/core/workspace.py
from dataclasses import dataclass

from pythonlings.core.curriculum import init_workspace


@dataclass(frozen=True)
class ResolvedWorkspace:
    root: Path
    created: bool


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
```

Place the `from dataclasses import dataclass` and `from pythonlings.core.curriculum import init_workspace` imports at the top of the module with the existing imports.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/unit/test_workspace.py -q`
Expected: PASS (8 passed).

- [ ] **Step 5: Commit**

```bash
git add pythonlings/core/workspace.py tests/unit/test_workspace.py
git commit -m "feat: add resolve_workspace_root precedence resolver"
```

---

### Task 3: Friendlier `init` messages

**Files:**
- Modify: `pythonlings/core/curriculum.py:81-82` (error text)
- Modify: `pythonlings/cli.py:84-93` (`_cmd_init`)
- Test: `tests/integration/test_cli_workspace.py`

**Interfaces:**
- Consumes: `is_workspace` (Task 1).
- Behavior: init on an existing workspace → friendly, exit 0; init on a non-empty non-workspace dir → actionable error, exit 1; empty/new → scaffold, exit 0.

- [ ] **Step 1: Update the existing test and add two new ones**

Replace `test_init_command_requires_force_for_non_empty_directory` and add the two below in `tests/integration/test_cli_workspace.py`:

```python
def test_init_rejects_non_empty_non_workspace_dir(tmp_path: Path, capsys) -> None:
    target = tmp_path / "stuff"
    target.mkdir()
    (target / "notes.txt").write_text("keep", encoding="utf-8")

    code = main(["init", "--path", str(target)])

    assert code == 1
    err = capsys.readouterr().err
    assert "isn't empty and isn't a pythonlings workspace" in err


def test_init_on_existing_workspace_is_friendly_noop(tmp_path: Path, capsys) -> None:
    target = tmp_path / "ws"
    assert main(["init", "--path", str(target)]) == 0
    capsys.readouterr()  # discard first output

    code = main(["init", "--path", str(target)])

    assert code == 0
    assert "Already set up" in capsys.readouterr().out


def test_init_force_overwrites_existing_workspace(tmp_path: Path) -> None:
    target = tmp_path / "ws"
    assert main(["init", "--path", str(target)]) == 0
    code = main(["init", "--path", str(target), "--force"])
    assert code == 0
    assert (target / "info.toml").exists()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/integration/test_cli_workspace.py -q`
Expected: FAIL — old message assertion gone; `Already set up` not printed yet.

- [ ] **Step 3: Update the error message in `curriculum.py`**

Replace `pythonlings/core/curriculum.py:81-82`:

```python
    if path.exists() and any(path.iterdir()) and not force:
        raise WorkspaceError(
            f"{path} isn't empty and isn't a pythonlings workspace. "
            "Pick another location with --path <dir>, or --force to set up here anyway."
        )
```

- [ ] **Step 4: Update `_cmd_init` in `cli.py`**

Replace `pythonlings/cli.py:84-93`:

```python
def _cmd_init(path: Path, force: bool) -> int:
    from pythonlings.core.curriculum import WorkspaceError, init_workspace
    from pythonlings.core.workspace import is_workspace

    path = path.expanduser().resolve()
    if is_workspace(path) and not force:
        print(f"Already set up at {path} — just run `pythonlings`")
        return 0
    try:
        root = init_workspace(path, force=force)
    except WorkspaceError as e:
        sys.stderr.write(f"pythonlings: {e}\n")
        return 1
    print(f"Created your workspace at {root}")
    return 0
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/integration/test_cli_workspace.py -q`
Expected: PASS (all tests in the file).

- [ ] **Step 6: Commit**

```bash
git add pythonlings/core/curriculum.py pythonlings/cli.py tests/integration/test_cli_workspace.py
git commit -m "feat: make init messages actionable and idempotent"
```

---

### Task 4: Wire defaults + resolver into the CLI

**Files:**
- Modify: `pythonlings/cli.py` (`_build_parser` defaults; add `_display_path`; rewrite the resolution block in `main`)
- Test: `tests/integration/test_first_run.py` (new), `tests/integration/test_cli_workspace.py`

**Interfaces:**
- Consumes: `resolve_workspace_root`, `default_workspace_root` (Tasks 1-2).
- Behavior: bare `pythonlings`/`watch`/`start`/`topics` create the home workspace if none is found, print a one-line notice, and launch the TUI on the resolved root. All other root commands resolve cwd-workspace → home-workspace (no create). `init`/`update` with no `--path` default to the home workspace.

- [ ] **Step 1: Write the failing tests**

```python
# tests/integration/test_first_run.py
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/integration/test_first_run.py -q`
Expected: FAIL — `init` still defaults to cwd; bare run does not create/notice.

- [ ] **Step 3: Update parser defaults in `_build_parser`**

In `pythonlings/cli.py`, change line 24 (`--root` default) and lines 30 / 36 (`--path` defaults). First add the import near the top of the module (after the existing imports):

```python
from pythonlings.core.workspace import default_workspace_root
```

Then:

```python
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Workspace root containing info.toml (default: auto-resolve).",
    )
```

```python
    p_init.add_argument("--path", type=Path, default=default_workspace_root())
```

```python
    p_update.add_argument("--path", type=Path, default=default_workspace_root())
```

- [ ] **Step 4: Add the `_display_path` helper**

Add near `_resolve_topic` in `pythonlings/cli.py`:

```python
def _display_path(path: Path) -> str:
    """Render `path` with a leading `~/` when inside the home directory."""
    try:
        return "~/" + str(path.relative_to(Path.home()))
    except ValueError:
        return str(path)
```

- [ ] **Step 5: Rewrite the resolution + dispatch block in `main`**

Replace `pythonlings/cli.py:261-311` (from the migration comment through the watch branch) with:

```python
    from pythonlings.core.curriculum import migrate_legacy_state_dir
    from pythonlings.core.workspace import resolve_workspace_root

    try:
        root: Path | None = None
        if args.command in ("init", "update"):
            migrate_legacy_state_dir(Path(args.path))
        else:
            launches_tui = args.command in (None, "watch", "start", "topics")
            resolved = resolve_workspace_root(
                Path.cwd(), args.root, create_if_missing=launches_tui
            )
            root = resolved.root
            migrate_legacy_state_dir(root)
            if resolved.created:
                print(
                    f"Created your workspace at {_display_path(root)} "
                    "(edit in-app, or open that folder in your editor)"
                )

        if getattr(args, "debug", False) and root is not None:
            try:
                (root / ".pythonlings_debug.log").write_text(
                    f"argv={argv if argv is not None else sys.argv[1:]!r}\n",
                    encoding="utf-8",
                )
            except OSError:
                pass

        if args.command == "init":
            return _cmd_init(args.path, args.force)
        if args.command == "update":
            return _cmd_update(args.path)

        assert root is not None
        if args.command == "verify":
            return _cmd_verify(root, args.topic)
        if args.command == "list":
            return _cmd_list(root, args.topic)
        if args.command == "hint":
            return _cmd_hint(root, args.name)
        if args.command == "run":
            return _cmd_run(root, args.name)
        if args.command == "dry-run":
            return _cmd_run(root, args.name)
        if args.command in {"solution", "sol"}:
            return _cmd_solution(root, args.name)
        if args.command == "reset":
            return _cmd_reset(root, args.name, args.yes)

        if args.command in (None, "watch", "start", "topics"):
            start_topic = getattr(args, "topic", None)
            if start_topic is not None:
                from pythonlings.core.manifest import load as load_manifest
                if _resolve_topic(load_manifest(root), start_topic) is None:
                    return 2
            from pythonlings.app import run_tui  # lazy: Textual is heavy
            return run_tui(
                root,
                start_topic,
                force_picker=args.command == "topics",
            )

        # Other subcommands wired in later tasks.
        sys.stderr.write(f"pythonlings: '{args.command}' not implemented yet\n")
        return 1
```

Leave the existing `except Exception as e:` handler that follows it unchanged.

- [ ] **Step 6: Run the new tests, then the full suite**

Run: `python -m pytest tests/integration/test_first_run.py -q`
Expected: PASS (3 passed).

Run: `python -m pytest -q`
Expected: PASS (full suite). If a pre-existing test fails because it relied on `--root` defaulting to cwd while cwd is not a workspace, fix it by passing an explicit `--root` (matching prior intent).

- [ ] **Step 7: Commit**

```bash
git add pythonlings/cli.py tests/integration/test_first_run.py
git commit -m "feat: auto-resolve and auto-create the workspace for bare pythonlings"
```

---

### Task 5: Docs + version bump to 0.4.0

**Files:**
- Modify: `Readme.md:19-25` (quick-start), `Readme.md:30` (status), `Readme.md:52-53` (step 1)
- Modify: `pyproject.toml:7` (version)
- Modify: `CHANGELOG.md` (new `[0.4.0]` entry)

**Interfaces:** none (docs/metadata only).

- [ ] **Step 1: Update the README quick-start**

Replace `Readme.md:19-25`:

```markdown
**Try it in 10 seconds** — zero install, needs [Python 3.9+](https://www.python.org/downloads/)
and [uv](https://docs.astral.sh/uv/):

```bash
uvx pythonlings
```
```

Replace `Readme.md:30`:

```markdown
Status: `v0.4.0`, alpha — published on PyPI as `pythonlings`.
```

Replace `Readme.md:52-53` (step 1 of "What Happens When You Run It"):

```markdown
1. `pythonlings` with no workspace creates a self-contained one at
   `~/.pythonlings` (override with `PYTHONLINGS_HOME` or `pythonlings init
   --path <dir>`) and opens the first exercise.
```

- [ ] **Step 2: Bump the version**

Replace `pyproject.toml:7`:

```toml
version = "0.4.0"
```

- [ ] **Step 3: Add the CHANGELOG entry**

Insert above the most recent entry in `CHANGELOG.md` (after the intro paragraph that ends on line 4):

```markdown
## [0.4.0] - 2026-06-20

### Added

- Zero-config first run: `pythonlings` with no workspace creates one at
  `~/.pythonlings` and opens the first exercise — no `init`, no `--path`, no
  `cd` required.
- `PYTHONLINGS_HOME` environment variable to point the default workspace
  somewhere else.

### Changed

- `pythonlings init` with no `--path` now targets `~/.pythonlings` instead of
  the current directory, so it can no longer fail by landing in a folder full
  of unrelated files.
- `init` is now idempotent on an existing workspace (a friendly note instead of
  an error), and its non-empty-directory error explains how to proceed.
- Every command resolves its workspace the same way: an explicit `--root`, then
  the current directory if it is a workspace, then `~/.pythonlings`.

```

- [ ] **Step 4: Verify the build reports the new version**

Run:
```bash
python -m pytest -q
rm -rf dist && python -m build >/dev/null 2>&1
python -m pip install --force-reinstall dist/pythonlings-0.4.0-py3-none-any.whl >/dev/null
pythonlings --version
```
Expected: full suite PASS; `pythonlings 0.4.0`.

- [ ] **Step 5: Commit**

```bash
git add Readme.md pyproject.toml CHANGELOG.md
git commit -m "docs: document zero-config first run and bump to 0.4.0"
```

---

## Self-Review

**Spec coverage:**
- Default location `PYTHONLINGS_HOME`/`~/.pythonlings` → Task 1.
- `resolve_workspace_root` precedence (4 branches) → Task 2.
- `init` default → home; friendly/actionable messages → Tasks 3-4.
- One-line create notice + `~/.pythonlings` display form → Task 4 (`_display_path`).
- cwd-workspace-wins; `--root`/`--path` custom support preserved → Tasks 2, 4.
- Edge: home exists non-empty non-workspace → `init_workspace` raises the actionable error (Task 3) via the resolver's create branch; surfaces through the existing `except` handler.
- Unit tests (resolver, default root) + integration (init messaging, first run) with `run_tui` mocked → Tasks 1-4.
- Version 0.4.0 + CHANGELOG → Task 5.

**Placeholder scan:** none — every code/test step is complete.

**Type consistency:** `default_workspace_root() -> Path`, `is_workspace(Path) -> bool`, `ResolvedWorkspace(root, created)`, and `resolve_workspace_root(cwd, explicit_root=None, *, create_if_missing=False)` are used identically across Tasks 2 and 4. `_display_path(Path) -> str` used only in Task 4.

**Known risk:** changing `--root`'s default from `Path.cwd()` to `None` could surface a pre-existing test that ran a root command without `--root` from a non-workspace cwd. Task 4 Step 6 runs the full suite to catch it; the fix is to pass an explicit `--root`.
