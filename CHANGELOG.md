# Changelog

All notable changes to this project are documented here. Pythonlings follows
Semantic Versioning.

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

## [0.3.1] - 2026-06-20

### Fixed

- `pythonlings --version` now reports the installed package version instead of
  a separate hardcoded string in `cli.py` (which had drifted to `0.3.0`). The
  version is read from package metadata, so it can no longer fall out of sync
  with `pyproject.toml`.
- Corrected stale `pylings` references in the contributor guide (`CLAUDE.md`):
  the smoke-test command, manual-testing flows, package paths, stylesheet, and
  entry point now consistently use the `pythonlings` name the project adopted
  in 0.3.0. (The unrelated `pylings` PyPI package belongs to a different
  project; `pythonlings` is the only command this project ships.)

## [0.3.0] - 2026-06-10

### Added

- The in-app reference (`F5`) now bundles a second complementary section from
  the official Python documentation for every topic, roughly tripling each
  topic's offline reference content.

### Changed

- The project is renamed from pylings to **pythonlings**. The PyPI package
  (previously `python-learnings`), the CLI command (previously `pylings`),
  and the Python package are all now `pythonlings`. Existing workspaces are
  migrated automatically: a legacy `.pylings/` state directory is renamed to
  `.pythonlings/` on the next run, preserving progress and reset snapshots.
- The README and quick-start now describe the built-in editor accurately:
  checks rerun as you type in the TUI editor.

### Fixed

- Running `pythonlings` outside a workspace now explains how to create one
  with `pythonlings init` instead of a bare "info.toml not found".

### Removed

- The unused `watchdog` dependency, for a lighter install.

## [0.2.0] - 2026-05-30

### Added

- Support for Python 3.9 and 3.10 (minimum was 3.11), broadening
  compatibility with stock macOS and Debian/Ubuntu interpreters.

### Changed

- The `type_hints4`, `type_hints8`, and `itertools8` exercises carry a small
  forward-compatibility shim (`from __future__ import annotations` and a
  `tee`-based `pairwise` fallback) so their modern syntax and stdlib usage run
  on Python 3.9 and 3.10. The learner's task is unchanged.

### Fixed

- Manifest loading now falls back to the `tomli` backport on Python < 3.11,
  where `tomllib` is not available in the standard library. Previously the
  package would install but crash on launch under older interpreters.

## [0.1.0] - 2026-05-25

### Added

- Interactive Textual coding workflow with topic picker, resume state, hints,
  reset, and automatic check reruns.
- CLI commands for listing topics, running exercises, printing hints, resetting
  files, and verifying curricula.
- 292 Python exercises across 31 topics with mirrored hidden checks.
- Bundled local Python documentation snippets generated from official docs.
- In-app documentation modal with `F5`, `Esc`, and `O` keyboard flow.
- PyPI distribution name `pythonlings`, which installs the `pythonlings` command.
- Contributor guide, screenshots, release flow notes, and MIT license.

### Verified

- Full test suite: `125 passed`.
- Curriculum/docs audit: every exercise has a configured docs URL and a bundled
  local snippet.
