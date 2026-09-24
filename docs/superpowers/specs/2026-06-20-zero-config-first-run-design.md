# Zero-config first run for pythonlings

- **Date:** 2026-06-20
- **Status:** Approved design
- **Target release:** 0.4.0 (minor — new behavior)

## Problem

`pythonlings init` and bare `pythonlings` both default their target directory to
the current working directory (`Path.cwd()`):

- `init` scaffolds into cwd and aborts with `<path> already exists and is not
  empty` when cwd contains unrelated files. Observed in the wild: a user ran
  `pythonlings init` inside a folder full of `.mp4` screen recordings and got a
  cryptic failure.
- Bare `pythonlings` launches the TUI against cwd and only prints guidance when
  cwd lacks `info.toml`.

A brand-new user therefore has to know to create and enter a dedicated directory
before anything works. We want Rustlings-grade onboarding: install, type
`pythonlings`, start learning.

## Goals

- A first-time user runs `pythonlings` (no flags, from any directory) and lands
  in the first exercise.
- No prompts, no required `init`, no `--path`.
- Existing workflows keep working: `--root`, `--path`, running inside a
  workspace, and the test fixtures.
- `init`'s confusing non-empty error is replaced with actionable guidance.

## Non-goals

- An in-TUI welcome / onboarding screen (possible later; not required here).
- Changes to the curriculum, the state format, or the TUI editor.

## Design

### Default workspace location

- Default workspace root: the `PYTHONLINGS_HOME` environment variable if set,
  otherwise `~/.pythonlings` (a hidden folder).
- Why hidden: exercises are edited in the **built-in TUI editor** (checks rerun
  as you type), so a beginner never navigates to the files on disk. A hidden
  folder keeps `$HOME` clean. Power users who prefer their own editor pass an
  explicit `--path` / `--root` pointing at a visible location.
- Single source of truth: `default_workspace_root() -> Path` in `core/`. It
  reads `PYTHONLINGS_HOME` (expanded + resolved) and falls back to
  `Path.home() / ".pythonlings"`.
- Note: the in-workspace state dir is also named `.pythonlings/`, so state for
  the default workspace lands at `~/.pythonlings/.pythonlings/state.json`.
  Functional; no change to the state-dir convention.

### Workspace resolution (bare `pythonlings`, no `--root`)

A new `resolve_workspace_root(cwd, explicit_root=None)` in `core/` returns the
chosen root and whether it was just created (e.g. a small dataclass/namedtuple
`ResolvedWorkspace(root: Path, created: bool)`). Precedence:

1. **`explicit_root` given** (`--root`): use it as-is. Existing behavior — error
   later if it is not a workspace.
2. **cwd is a workspace** (`cwd/info.toml` exists): use cwd. Preserves "run
   inside a workspace", multiple workspaces, and the `--root` test fixtures.
3. **default home workspace exists** (`default_workspace_root()/info.toml`
   exists): resume it, silently.
4. **none of the above**: create a workspace at `default_workspace_root()` via
   `init_workspace`, and return `created=True`.

`cli.py` calls the resolver, prints the one-line create notice when `created`,
then launches the TUI. The TUI already resumes at the first unsolved exercise,
so a fresh workspace lands on `variables1` with no extra code.

### `init` changes

- `--path` default changes from `Path.cwd()` to `default_workspace_root()`.
- `_cmd_init` / `init_workspace` behavior by target state:
  - **Already a workspace** (`info.toml` present): print
    `` Already set up at <path> — just run `pythonlings` `` and exit `0` (not an
    error).
  - **Empty or nonexistent**: scaffold as today.
  - **Non-empty and NOT a workspace**: error with
    `<path> isn't empty and isn't a pythonlings workspace. Pick another location with --path <dir>, or --force to set up here anyway.`
    and a non-zero exit. This replaces today's cryptic message.
  - **`--force`**: scaffold regardless (unchanged).

### Messaging

- Create notice: `Created your workspace at <display-path> (edit in-app, or open that folder in your editor)`,
  where `<display-path>` renders the `~/.pythonlings` form rather than an
  absolute path.
- Resume: silent (just launch).

### Edge cases

- Default home root exists, non-empty, no `info.toml`: treated as the `init`
  non-workspace error (never clobber). Rare.
- Not a TTY: the resolver still creates the workspace; TUI launch behaves as it
  does today in non-interactive contexts (out of scope to change here).
- `PYTHONLINGS_HOME` set to a relative or `~`-prefixed path: resolved via
  `Path(...).expanduser().resolve()`.

## Affected code

- `core/` (`curriculum.py`, or a focused new `core/workspace.py`):
  `default_workspace_root()`, `resolve_workspace_root()`, and the friendlier
  `init_workspace` messaging.
- `cli.py`: `--path` / `--root` defaults; the bare-command resolver call + create
  notice; `_cmd_init` messaging.

## Testing

- **Unit** (`tests/unit/`):
  - `default_workspace_root()`: respects `PYTHONLINGS_HOME`; falls back to
    `~/.pythonlings` (monkeypatch env + `Path.home`).
  - `resolve_workspace_root()`: all four precedence branches (explicit root,
    cwd-workspace, existing home workspace, create-new), asserting the chosen
    root and the `created` flag, using `tmp_path` + monkeypatched home. No TUI.
  - `init` messaging: existing-workspace → friendly exit 0; non-empty
    non-workspace → actionable error; empty → scaffolds.
- **Integration** (`tests/integration/`): `pythonlings init` (no path) targets
  the monkeypatched home; bare run resolves correctly with `run_tui` patched.
- Keep `run_tui` mocked in CLI tests so Textual stays out of unit tests.

## Versioning

Minor feature → **0.4.0**. CHANGELOG entries under `Added` (zero-config first
run, `PYTHONLINGS_HOME`) and `Changed` (`init` default location + friendlier
errors).
