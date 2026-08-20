# Contributing to Pythonlings

Welcome! Pythonlings is actively developed and welcomes contributors — beginners included.

## Where to start

The current focus is the [August 2026 Community Dev Sprint](https://github.com/abhiksark/pythonlings/issues/52).
Start with a [`good first issue`](https://github.com/abhiksark/pythonlings/issues?q=is%3Aopen+label%3A%22good+first+issue%22),
comment to claim it, and read this guide.

## Development setup

```bash
git clone git@github.com:abhiksark/pythonlings.git
cd pythonlings
pip install -e ".[dev]"
python -m pytest -q
