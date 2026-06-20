# Roadmap

Pythonlings is `v0.3.1`, published on PyPI as `pythonlings`. Install with
`uvx pythonlings` or `pip install pythonlings`.

## Shipped in v0.3.x

- 292 exercises across 31 topics.
- Live Textual editor and automatic checks.
- Topic picker, progress state, reset, hints, and CLI commands.
- Bundled Python docs snippets with official docs links.
- Published on PyPI as `pythonlings`; canonical install is `uvx pythonlings`.

## Next Work

- Improve first-run onboarding and empty-state copy.
- Harden keyboard flow around `Enter`, `Esc`, `F4`, and `F5`.
- Add more TUI tests for the coding screen, docs window, and topic picker.
- Add a release smoke test that installs the built wheel and exercises the CLI.
- Continue auditing exercises for clearer hints and stronger hidden checks.

## Release Policy

Pythonlings follows Semantic Versioning.

- `MAJOR`: incompatible curriculum or CLI changes.
- `MINOR`: new topics, exercises, TUI features, or docs workflows.
- `PATCH`: fixes, copy edits, compatible tests, and packaging updates.
