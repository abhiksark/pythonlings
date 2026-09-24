<!-- CONTRIBUTING.md -->
# Contributing

Pythonlings is actively developed and **open to contributors** — beginners welcome.
The fastest way in is a [`good first issue`](https://github.com/abhiksark/pythonlings/issues?q=is%3Aopen+label%3A%22good+first+issue%22).

## Community

- **Chat:** BangPypers hosts the Pythonlings channel on Discord —
  [join here](https://discord.gg/JVrYn5fH2). Remote contributors coordinate
  there during dev sprints, and it is the fastest place to ask a question.
- **Discussions:**
  [GitHub Discussions](https://github.com/abhiksark/pythonlings/discussions)
  for questions, ideas, and exercise proposals.
- **Sprints:** in-person and online sessions are announced as discussions, such
  as the
  [August 2026 Community Dev Sprint](https://github.com/abhiksark/pythonlings/discussions/37).

## Where the work is

- Track current work in the
  [open issue tracker](https://github.com/abhiksark/pythonlings/issues?q=is%3Aissue+is%3Aopen).
- Find contributor-ready work by label: [`good first issue`](https://github.com/abhiksark/pythonlings/issues?q=is%3Aopen+label%3A%22good+first+issue%22),
  [`help wanted`](https://github.com/abhiksark/pythonlings/issues?q=is%3Aopen+label%3A%22help+wanted%22).

## Claiming an issue

1. Comment on the issue to claim it (e.g. "I'd like to take this"). This avoids
   two people doing the same work.
2. Ask any questions right on the issue — happy to clarify scope.
3. Open a PR that references the issue (`Closes #NN`).

No need to wait for a formal assignment; claiming by comment is enough.

## Proposing a new exercise

Have an idea for a tiny broken program — especially one covering newer Python
features the curriculum does not reach yet? Open an
[Exercise Proposal](https://github.com/abhiksark/pythonlings/discussions/new?category=exercise-proposals).

Proposals are **discussions, not issues**. Anyone can open one, no permissions
needed, and nothing lands in the issue tracker until a maintainer converts an
accepted proposal into a scoped issue that anyone can then claim.

You do not need working code to propose an idea. A clear statement of what the
learner should come away knowing is enough to start; the form asks for a draft
exercise, check, and reference solution, but all three are optional.

Before proposing, check the concept is not already covered — `pythonlings list`
shows every exercise, and [`info.toml`](info.toml) is the manifest in curriculum
order.

## Development Setup

```bash
git clone git@github.com:abhiksark/pythonlings.git
cd pythonlings
pip install -e ".[dev]"   # or: uv pip install -e ".[dev]"
python -m pytest -q
```

Supported Python: 3.9+.

## Curriculum Changes

Every exercise is five artifacts that must stay in sync:

```text
exercises/<topic>/<name>.py   the broken program the learner edits
checks/<topic>/<name>.py      bare asserts run against it
solutions/<name>.py           a two-line loader, flat with no topic directory
solutions/_answers.py         the reference solution itself, keyed by name
info.toml                     name, path, hint, docs URL, and curriculum order
```

Only `name` and `path` are recorded in `info.toml`. The check path is derived by
replacing the first path segment, and the solution is resolved by name alone —
so moving an exercise between topic directories silently breaks its check, and
renaming a solution file silently changes which answer runs.

### Writing exercises

- Keep the `# I AM NOT DONE` marker. It gates advancement, and it is a plain
  substring search over the whole file — a marker inside a string literal keeps
  the exercise permanently pending.
- Curriculum code is copied verbatim into every learner workspace, so it must be
  self-contained and cannot import from the repository.
- Exercise names and their order in `info.toml` are learner-facing. Renaming or
  reordering them breaks saved progress.

### Writing checks

- Use bare module-level asserts that read the exercise's names directly. No test
  function, and never import the exercise — the runner executes both files in
  one shared namespace.
- Every assert needs a message stating the **expected value**, not the
  computation. `"sum_ac should be str(a) + c"` only restates the code;
  `"sum_ac should be '10hello'"` tells a stuck learner something.
- Report the actual value where it is cheap, but never re-call the learner's
  function inside the message — that re-runs their code, which can corrupt call
  counters or mask the failure.
- Begin the file with its own path as a comment: `# checks/<topic>/<name>.py`.
- Keep lines to 80 characters or fewer.
- End with `print("<name> ✓")`.

### Before opening the pull request

Adding or removing an exercise changes counts pinned in the tests:
`tests/unit/test_manifest.py` asserts the total exercise count, the topic count,
and per-topic counts. Update them in the same commit.

```bash
python -m pytest -q
pythonlings --root tests/fixtures/passing_curriculum verify
python -m pytest tests/integration/test_solution_verify.py -q
```

## Pull Requests

- Create focused branches from the current `dev` branch, named
  `feature/<name>` or `fix/<name>`.
- Open pull requests against `dev`. Feature and fix pull requests are
  squash-merged after CI passes and review feedback is resolved.
- Reference the issue you're closing (`Closes #NN`).
- Include a short description, test output (`python -m pytest -q`), and
  screenshots/GIFs for TUI changes.
- Keep PRs scoped to one issue where possible.

## Release Flow

```text
feature/<name> or fix/<name> -> dev -> main -> vMAJOR.MINOR.PATCH
```

Maintainers promote a verified `dev` branch to `main` with a merge commit, not
a squash merge. The release tag is created from the exact promoted commit on
`main`; see [RELEASE.md](RELEASE.md) for the release checklist.
