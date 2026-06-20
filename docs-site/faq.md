# FAQ

## How is this different from Rustlings?

Pythonlings brings the same fix-broken-exercises idea to Python. Instead of Rust's compiler, it uses a terminal TUI built with [Textual](https://textual.textualize.io/) and runs hidden `assert`-based checks in a subprocess each time you save.

## Do I need `uv`?

No. The easiest zero-install path is `uvx pythonlings`, but you can also install with `pipx install pythonlings`, `uv tool install pythonlings`, or plain `pip install pythonlings`.

## Which Python versions are supported?

Python 3.9 and above (`requires-python = ">=3.9"`).

## Where is my progress stored?

Progress lives in the learner workspace you create with `pythonlings init`, at `<workspace>/.pythonlings/state.json`. It is written atomically with a `.bak` recovery copy and is never stored inside the installed package.

## How do I update or reset?

Run `pythonlings update` to pull the latest exercises into an existing workspace. To restore a single exercise to its original broken state, run `pythonlings reset <exercise> --yes`.

## Does it work offline?

Yes. All exercises and the bundled local Python reference (press `F5` in the TUI) work without a network connection. Only the "open official docs" shortcut (`O`) requires internet access.

## Is Pythonlings on PyPI?

Yes — install it as [`pythonlings`](https://pypi.org/project/pythonlings/) (current release: `v0.3.1`).

## How do I see the reference answer?

Run `pythonlings solution <exercise>` (alias: `sol`). This executes the reference solution for the named exercise.
