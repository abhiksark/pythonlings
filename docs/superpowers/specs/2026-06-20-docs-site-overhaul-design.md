# Docs-site overhaul — design spec

**Date:** 2026-06-20
**Branch:** `feature/docs-site-overhaul`
**Scope:** The MkDocs site in `docs-site/` published to `https://pythonlings.abhik.ai/`. No application/curriculum code changes.

## Problem

The published docs site has drifted badly from reality:

- It advertises **`v0.1.0` alpha**, says the **PyPI name is "reserved"**, and tells users to install a **GitHub tag** (`pipx install "git+…@v0.1.0"`). In reality `pythonlings` is **published on PyPI at `v0.3.1`**, and the canonical install is `uvx pythonlings`.
- It is visually the stock MkDocs Material default: no hero, no dark mode, no brand identity, no social-share cards.
- It omits a first-timer "how the loop works" walkthrough and an FAQ.
- The `Readme.md` is already accurate and well-written; the site simply needs to catch up to it and then surpass it visually.

## Goals

1. Every install command, version string, and status line is correct and matches `Readme.md` + the real CLI.
2. A branded, intentional look: Python-blue/yellow palette, light/dark toggle, a custom centered homepage hero, logo/favicon, and social-share cards.
3. A clear first-time path with two new pages (How It Works, FAQ).
4. `mkdocs build --strict` stays green; the live custom domain (`pythonlings.abhik.ai`) is unaffected.

## Non-goals

- No changes to exercises, checks, solutions, `info.toml`, or the application package.
- No migration off MkDocs Material.
- No new top-level marketing landing page separate from the docs (that was Approach 2, explicitly not chosen).

## Locked design decisions

- **Approach:** "Catch up to the README, then polish" (full overhaul, single coherent pass).
- **Palette:** Python Classic — primary blue `#3776AB`, accent yellow `#FFD43B`, with a light + dark scheme toggle.
- **Hero:** Centered layout — eyebrow → tagline → subtitle → install pill → two CTAs → stat row → demo GIF.
- **Logo/favicon:** included — small SVG mark (a `>_` terminal prompt in blue with a yellow check) + "Pythonlings" wordmark.
- **Social cards:** included — Material `social` plugin (auto OG images), with the required imaging deps added to the docs requirements and the Pages CI workflow.

## Ground-truth facts (verified)

- Curriculum: **292 exercises across 31 topics** (current `curriculum.md` counts are correct).
- PyPI: `pythonlings` latest **`0.3.1`**; `pyproject.toml` version `0.3.1`.
- Canonical install (from `Readme.md`): `uvx pythonlings`; alternatives `pipx install pythonlings`, `uv tool install pythonlings`, `pip install pythonlings`.
- Real CLI subcommands (`pythonlings/cli.py`): `init, run, dry-run, hint, list, topics, reset, update, start, watch`. **Action:** reconcile docs against `pythonlings --help` during the build — confirm/replace any reference to `solution`/`verify` and document `start`/`watch` if user-facing.
- Existing assets: `docs/assets/demos/pythonlings-demo.gif`, plus `coding-screen.png`, `topic-picker.png`, `docs-reference.png`.

## Plan by area

### A. Theme & visual

- **New** `docs-site/stylesheets/extra.css`: define exact palette via Material CSS custom properties (`--md-primary-fg-color`, `--md-accent-fg-color`, etc.) for both light and dark schemes; hero classes (eyebrow, H1, subtitle, install pill, CTA buttons, stat row); spacing/typography polish.
- **New** `docs-site/assets/` (or `docs-site/images/`): SVG logo mark + wordmark + favicon (`.svg`/`.png`).
- `mkdocs.yml`: add `palette` with two schemes + toggle; `font` (text: Inter, code: JetBrains Mono); `logo` + `favicon`; `extra_css`; features (`navigation.instant`, `navigation.footer`, `content.code.copy`, `content.tabs.link`, `search.suggest`/`search.highlight`); `extra.social` (GitHub, PyPI); `copyright`.
- **Hero** is authored in `index.md` as HTML blocks (the project already enables `md_in_html` + `attr_list`), styled by `extra.css`. No theme template override — keeps maintenance low.

### B. Content accuracy

- `index.md`: replace top with the new hero; remove every stale string (`v0.1.0`, "reserved", "until the PyPI release is live", GitHub-tag install). Lead install with `uvx pythonlings init`. "Project Status" → `v0.3.1`, published on PyPI.
- `quick-start.md`: lead with `uvx pythonlings init`; show install alternatives (pipx / uv tool / pip) in tabbed blocks; fix "after PyPI publishing is enabled" copy; audit the command list against `--help`.
- `interface.md`: verify every keybinding and command against the running app; add `start`/`watch` if user-facing; correct anything stale.
- `roadmap.md`: mark PyPI publishing as shipped; reflect the 0.3.x state; keep forward-looking items that are still true.
- `curriculum.md`, `local-docs.md`, `contributing.md`: light polish; confirm counts and commands.

### C. Structure & new content

- Nav reorder (first-timer path): **Home → Quick Start → How It Works → Interface → Curriculum → Local Docs → FAQ → Contributing → Roadmap.**
- **New** `docs-site/how-it-works.md`: the edit→check→advance loop, the `# I AM NOT DONE` marker, a worked broken→fixed→green example, where progress is stored (`<workspace>/.pythonlings/state.json`), the demo GIF.
- **New** `docs-site/faq.md`: vs Rustlings; do I need `uv`; Python 3.9+ support; where progress lives; how to update/reset; offline docs; is it on PyPI.

### D. Build / SEO / CI

- `requirements-docs.txt`: `mkdocs-material[imaging]>=9.5` (enables social cards).
- `mkdocs.yml` `plugins`: `search`, `social`.
- `.github/workflows/pages.yml`: install the system libraries the `social` plugin needs (cairo/pango/freetype via `apt-get`) before `mkdocs build`.
- Keep `docs-site/CNAME`, root `CNAME`, and `docs-site/robots.txt` exactly as-is; MkDocs continues to emit `sitemap.xml`.
- `markdown_extensions`: add `pymdownx.tabbed` (install tabs), `pymdownx.details`, `pymdownx.emoji`; keep existing.

## Verification

1. `mkdocs build --strict` is green (strict catches broken internal links from the nav reorder).
2. `mkdocs serve` local preview: hero renders, dark-mode toggle works, social card generates, every nav link resolves.
3. `grep -ri "v0.1.0\|reserved for PyPI\|PyPI release is live\|@v0.1.0" docs-site/` returns nothing.
4. Every install command in the site matches `Readme.md`; every CLI command/keybinding matches `pythonlings --help` and the app.
5. The Pages workflow builds successfully (social-card deps install cleanly) — verified by re-reading the workflow logic; actual deploy happens on merge to `main`.

## Risks & mitigations

- **Social-card CI deps** are the most likely build breakage (cairo/pango on the runner). Mitigation: pin the `apt-get` install in `pages.yml`; if it proves flaky, the `social` plugin can be gated behind a CI-only check without blocking the rest.
- **Nav reorder breaks links** under `--strict`. Mitigation: run `--strict` as the gate and fix every reported link.
- **Worktree stability:** this work is isolated in a manual `git worktree` under `.worktrees/` (a prior native worktree was auto-garbage-collected while empty); committing early anchors it.

## Out-of-scope follow-ups (noted, not done here)

- A bespoke animated landing page (Approach 2).
- Versioned docs (`mike`).
- Search analytics / feedback widgets.
