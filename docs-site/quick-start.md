# Quick Start

> Current release: **v0.3.1** · [PyPI](https://pypi.org/project/pythonlings/)

## Zero-Install (uvx)

No installation required — run Pythonlings directly with [uv](https://docs.astral.sh/uv/):

```bash
uvx pythonlings init --path ~/pythonlings-workspace
cd ~/pythonlings-workspace
uvx pythonlings
```

## Install Options

=== "uv (recommended)"
    ```bash
    uvx pythonlings            # zero-install, always latest
    uv tool install pythonlings
    ```

=== "pipx"
    ```bash
    pipx install pythonlings
    ```

=== "pip"
    ```bash
    pip install pythonlings
    ```

## Create a Workspace

```bash
pythonlings init --path ~/pythonlings-workspace
cd ~/pythonlings-workspace
pythonlings
```

`pythonlings init` copies exercises, hidden checks, reference solutions, and reset
snapshots into a self-contained learner workspace. Running `pythonlings` (or
`pythonlings watch`) from that workspace opens the first pending exercise in the
TUI.

## Useful Commands

```bash
pythonlings list                 # show all topics and progress
pythonlings topics               # open the topic picker in the TUI
pythonlings start variables      # launch TUI on a specific topic
pythonlings hint variables1      # print the hint for an exercise
pythonlings solution variables1  # run the reference solution for an exercise
pythonlings run variables1       # run a single exercise and show output
pythonlings dry-run variables1   # non-interactive run (CI-friendly)
pythonlings reset variables1 --yes  # restore exercise to its original state
pythonlings update               # pull new exercises into an existing workspace
```

## Exercise Loop

Each exercise contains a `# I AM NOT DONE` marker. Open the file in the TUI
editor (or any editor), fix the broken code, then remove the marker. Pythonlings
runs the hidden check automatically; when the check passes and the marker is gone,
the exercise is marked complete and progress advances to the next one.
