<!-- AGENTS.md -->
# AGENTS.md

## Scope

This guide applies to the entire repository. It is the canonical operational
policy for contributors and coding agents.

- Before editing `docs-site/**`, also read `docs-site/AGENTS.md`.
- Before editing `pythonlings/docs/**` or its generator, also read
  `pythonlings/docs/AGENTS.md`.
- Nested guides add local requirements; this root guide still applies.
- Treat `.pythonlings/` as ignored learner runtime state, not repository source.

## Supported Commands

Run commands from the repository root.

- Install development dependencies: `python -m pip install -e ".[dev]"`
- Run a targeted test: `python -m pytest tests/unit/test_runner.py -q`
- Run the full suite: `python -m pytest -q`
- Verify a passing curriculum:
  `pythonlings --root tests/fixtures/passing_curriculum verify`
- Install the packaging frontend: `python -m pip install build`
- Build the source and wheel distributions: `python -m build`

## Pull Request Validation

Every pull request must run:

- `python -m pytest -q`
- `pythonlings --root tests/fixtures/passing_curriculum verify`

Add the checks that match the change:

- Packaging, curriculum, or workspace changes: install `build`, run
  `python -m build`, run
  `python -m pip install --force-reinstall dist/pythonlings-*.whl`, and exercise
  the relevant installed flow.
- CLI changes: run the relevant tests under `tests/integration/` and include
  representative command output.
- TUI changes: run the relevant tests under `tests/tui/` and include current
  screenshots or GIFs of the affected flow.
- Documentation changes: follow the applicable nested `AGENTS.md`.

Record the exact commands and their results in the pull request description.

## Branch and Merge Policy

- Follow `CONTRIBUTING.md` for branch naming, pull request content, and the
  contributor workflow.
- Branch from the current `dev` using `feature/<name>` or `fix/<name>`, and
  target pull requests to `dev`.
- Keep pull requests in draft until local validation is complete and recorded.
- Squash-merge feature and fix pull requests into `dev` only after CI passes and
  review feedback is resolved.
- Promote a verified `dev` branch to `main` with a merge commit. Do not squash
  the `dev` to `main` release promotion.
- Never merge or enable auto-merge without explicit maintainer approval.

## Compatibility and Architecture

- Maintain Python 3.9 compatibility. Guard standard-library APIs introduced in
  newer Python versions and preserve required fallbacks.
- Keep Textual imports out of `pythonlings/core/` and one-shot CLI command import
  paths. Core behavior must remain usable without loading the TUI.
- Preserve the runner's isolated subprocess, five-second default timeout,
  shared exercise/check namespace, and `# I AM NOT DONE` completion marker.
- Preserve atomic state writes and corrupt-state backup. Do not discard learner
  progress when changing state handling.
- Preserve learner-edited exercises during workspace updates. Reset snapshots
  and bundled curriculum updates must not overwrite learner work implicitly.

## Learner and Curriculum Contract

Exercise names and their order in `info.toml` are learner-facing compatibility.
Avoid renaming, reordering, or removing them without an explicit migration.

For each curriculum change, keep all of these synchronized:

- `exercises/<topic>/<name>.py`
- the mirrored `checks/<topic>/<name>.py`
- `solutions/<name>.py`, which is a reference-solution loader
- the corresponding answer in `solutions/_answers.py`
- the hint, documentation URL, and ordered manifest entry in `info.toml`

Keep learner exercise files intentionally incomplete with `# I AM NOT DONE`.
Checks must use bare assertions with actionable, beginner-facing messages. Keep
curriculum code self-contained because it is copied into learner workspaces.

For changed learner exercises, confirm the marker remains present and run
`python -m pytest tests/integration/test_solution_verify.py -q` to prove their
reference solutions pass.

## Security and Releases

- Report vulnerabilities privately. Never disclose them through public issues
  or pull requests; follow `SECURITY.md`.
- Use only `pythonlings` as the distribution name. Do not publish or document
  this repository under a different package name.
- Read `RELEASE.md` before changing versions, tags, release workflows, or
  publishing behavior.
