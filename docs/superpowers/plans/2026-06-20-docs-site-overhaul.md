# Docs-site Overhaul Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the MkDocs site (`docs-site/`, published to pythonlings.abhik.ai) up to date with reality and give it a branded, intentional look.

**Architecture:** Pure docs/config changes to the existing MkDocs Material site. Visual identity via a new `extra.css` (CSS-var palette overrides) + SVG logo; a centered homepage hero authored as HTML in `index.md` (no theme template override); two new content pages; nav reorder; social-share cards gated to CI. No application or curriculum code is touched.

**Tech Stack:** MkDocs + Material for MkDocs (`mkdocs-material`), `pymdownx` extensions, Material `social` plugin (Pillow/Cairo imaging), GitHub Actions Pages deploy.

## Global Constraints

- **Scope:** only files under `docs-site/`, plus `mkdocs.yml`, `requirements-docs.txt`, `.github/workflows/pages.yml`. Never touch `exercises/`, `checks/`, `solutions/`, `info.toml`, or `pythonlings/`.
- **Canonical install command:** `uvx pythonlings` (zero-install). Alternatives, in this order: `pipx install pythonlings`, `uv tool install pythonlings`, `pip install pythonlings`.
- **Version/status copy:** the project is `v0.3.1`, **published on PyPI** as `pythonlings`. Never write `v0.1.0`, "reserved for PyPI", "until the PyPI release is live", or any `git+https://…@v0.1.0` install line.
- **Curriculum counts:** 292 exercises across 31 topics.
- **Build gate:** `mkdocs build --strict` must pass after every task (strict treats broken links / orphaned pages as errors).
- **Leave untouched:** `docs-site/CNAME`, root `CNAME`, `docs-site/robots.txt`.
- **Commits:** conventional prefixes; do NOT push (the user pushes); no "Claude"/"Generated with" lines in commit messages.
- **Worktree:** all work happens in `.worktrees/docs-site-overhaul` on branch `feature/docs-site-overhaul`.

**Verification environment (used by every task):** a docs venv lives at `.worktrees/docs-site-overhaul/.venv-docs` (gitignored, created in Task 1). Activate it before any `mkdocs` command:
```bash
source .venv-docs/bin/activate
```
All `mkdocs` commands below are run from the worktree root.

---

### Task 1: Theme foundation — palette, dark mode, fonts, extra.css

**Files:**
- Create: `docs-site/stylesheets/extra.css`
- Modify: `mkdocs.yml` (palette, font, features, `extra_css`)
- Modify: `.gitignore` (ignore docs venv)

**Interfaces:**
- Produces: CSS custom-property palette (`--md-primary-fg-color: #3776AB`, `--md-accent-fg-color`) and a set of hero utility classes (`.pl-hero`, `.pl-eyebrow`, `.pl-title`, `.pl-subtitle`, `.pl-install`, `.pl-ctas`, `.pl-btn`, `.pl-btn--ghost`, `.pl-stats`) consumed by Task 3.

- [ ] **Step 1: Create the docs venv and confirm a clean baseline build**

```bash
cd .worktrees/docs-site-overhaul    # if not already here
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements-docs.txt
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: build finishes with `0` warnings/errors (exit 0).

- [ ] **Step 2: Ignore the venv**

Append to `.gitignore`:
```
.venv-docs/
```

- [ ] **Step 3: Add palette, font, and features to `mkdocs.yml`**

Replace the existing `theme:` block's `palette` (currently a single scheme) with a light+dark toggle, and add fonts. The `theme:` block becomes:
```yaml
theme:
  name: material
  language: en
  logo: assets/logo.svg
  favicon: assets/favicon.svg
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.instant
    - navigation.sections
    - navigation.top
    - navigation.footer
    - content.code.copy
    - content.tabs.link
    - search.highlight
    - search.suggest
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
```
(The `logo`/`favicon` files are created in Task 2; reference them now — they resolve before Task 1's commit only if present, so if Task 1 is committed before Task 2, temporarily omit the `logo`/`favicon` lines and add them in Task 2. Prefer doing Task 2 immediately after.)

Add at the end of `mkdocs.yml`:
```yaml
extra_css:
  - stylesheets/extra.css
```

- [ ] **Step 4: Write `docs-site/stylesheets/extra.css`**

```css
:root {
  --md-primary-fg-color:        #3776AB;
  --md-primary-fg-color--light: #4f8fc0;
  --md-primary-fg-color--dark:  #2b5d88;
  --md-accent-fg-color:         #d9a400;   /* readable amber on light */
  --md-typeset-a-color:         #3776AB;
}
[data-md-color-scheme="slate"] {
  --md-primary-fg-color: #4f8fc0;
  --md-accent-fg-color:  #FFD43B;
  --md-typeset-a-color:  #7fc1ff;
}
/* Hero (consumed by index.md in Task 3) */
.pl-hero { text-align: center; padding: 2.5rem 1rem 1rem; }
.pl-eyebrow { font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  font-size: .72rem; color: var(--md-primary-fg-color); }
.pl-title { font-size: 2.2rem; line-height: 1.15; font-weight: 800; margin: .6rem auto .4rem;
  max-width: 18ch; }
.pl-subtitle { font-size: 1.05rem; color: var(--md-default-fg-color--light);
  max-width: 46ch; margin: 0 auto 1.2rem; }
.pl-install { display: inline-block; font-family: var(--md-code-font-family); font-weight: 600;
  background: #0F2436; color: #FFD43B; padding: .6rem .9rem; border-radius: 8px; }
.pl-ctas { display: flex; gap: .6rem; justify-content: center; flex-wrap: wrap; margin: 1.1rem 0; }
.pl-btn { display: inline-block; font-weight: 700; padding: .65rem 1.1rem; border-radius: 8px;
  background: var(--md-primary-fg-color); color: #fff !important; }
.pl-btn--ghost { background: transparent; color: var(--md-primary-fg-color) !important;
  border: 1.5px solid var(--md-primary-fg-color); }
.pl-stats { display: flex; gap: 1.4rem; justify-content: center; flex-wrap: wrap;
  font-weight: 600; color: var(--md-default-fg-color--light); margin-top: .4rem; }
.pl-stats b { color: var(--md-primary-fg-color); }
```

- [ ] **Step 5: Build and visually verify**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: exit 0, no warnings. Optionally `mkdocs serve` and confirm the light/dark toggle appears and links are blue.

- [ ] **Step 6: Commit**

```bash
git add mkdocs.yml docs-site/stylesheets/extra.css .gitignore
git commit -m "feat(docs): add custom palette, dark mode, and fonts"
```

---

### Task 2: Logo, wordmark, and favicon

**Files:**
- Create: `docs-site/assets/logo.svg`
- Create: `docs-site/assets/favicon.svg`
- Modify: `mkdocs.yml` (ensure `logo:`/`favicon:` lines present — added in Task 1)

**Interfaces:**
- Produces: `assets/logo.svg` (header wordmark+mark) and `assets/favicon.svg` (square mark) referenced by `theme.logo`/`theme.favicon`.

- [ ] **Step 1: Create `docs-site/assets/favicon.svg`** (square `>_ ✓` mark)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="12" fill="#3776AB"/>
  <path d="M16 22l9 10-9 10" fill="none" stroke="#FFD43B" stroke-width="5"
    stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="30" y="40" width="18" height="5" rx="2.5" fill="#FFD43B"/>
</svg>
```

- [ ] **Step 2: Create `docs-site/assets/logo.svg`** (header mark; Material renders it small in the header)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <path d="M16 22l9 10-9 10" fill="none" stroke="#FFD43B" stroke-width="5"
    stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="30" y="40" width="18" height="5" rx="2.5" fill="#FFD43B"/>
</svg>
```
(Header background is the primary blue, so the mark uses yellow strokes with no blue plate.)

- [ ] **Step 3: Confirm `mkdocs.yml` references them** — `theme.logo: assets/logo.svg` and `theme.favicon: assets/favicon.svg` (added in Task 1). Add now if they were omitted.

- [ ] **Step 4: Build**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: exit 0. (`mkdocs serve` → mark visible top-left, browser tab shows favicon.)

- [ ] **Step 5: Commit**

```bash
git add docs-site/assets/logo.svg docs-site/assets/favicon.svg mkdocs.yml
git commit -m "feat(docs): add logo mark and favicon"
```

---

### Task 3: Homepage hero + index accuracy

**Files:**
- Modify: `docs-site/index.md`

**Interfaces:**
- Consumes: hero classes from Task 1's `extra.css`.

- [ ] **Step 1: Rewrite `docs-site/index.md`**

Front matter hides the TOC for a landing feel; hero is raw HTML (works because `md_in_html`/`attr_list` are enabled). Below the hero, keep accurate markdown sections.
```markdown
---
hide:
  - toc
---

<div class="pl-hero" markdown>
  <div class="pl-eyebrow">Rustlings for Python</div>
  <div class="pl-title">Learn Python by fixing tiny broken programs.</div>
  <div class="pl-subtitle">292 exercises across 31 topics. Hidden checks rerun the
    instant you save — fix the code, watch it go green, advance.</div>
  <div class="pl-install">$ uvx pythonlings init</div>
  <div class="pl-ctas">
    <a class="pl-btn" href="quick-start/">Get started →</a>
    <a class="pl-btn pl-btn--ghost" href="https://github.com/abhiksark/pythonlings">View on GitHub</a>
  </div>
  <div class="pl-stats"><span><b>292</b> exercises</span><span><b>31</b> topics</span><span><b>zero</b> setup</span></div>
</div>

![Pythonlings terminal demo](https://raw.githubusercontent.com/abhiksark/pythonlings/main/docs/assets/demos/pythonlings-demo.gif)

## What you get

- Rustlings-inspired Python practice, entirely in your terminal.
- Hidden checks that rerun as you type and advance you automatically.
- Topic picker, progress tracking, reset, progressive hints, and one-shot CLI commands.
- A local docs window with links back to the official Python documentation.
- A self-contained learner workspace created by `pythonlings init`.

## Start here

```bash
uvx pythonlings init --path ~/pythonlings-workspace
cd ~/pythonlings-workspace
uvx pythonlings
```

Prefer a permanent install? See [Quick Start](quick-start.md) for `pipx`, `uv tool`, and `pip`.

## Project status

Pythonlings is `v0.3.1`, published on PyPI as `pythonlings`. The learner loop, CLI, and
curriculum are stable; see the [Roadmap](roadmap.md) for what's next.
```

- [ ] **Step 2: Build + check no stale strings**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
grep -riE "v0\.1\.0|reserved for PyPI|PyPI release is live|@v0\.1\.0" docs-site/index.md
```
Expected: build exit 0; grep prints nothing.

- [ ] **Step 3: Commit**

```bash
git add docs-site/index.md
git commit -m "feat(docs): add homepage hero and correct install/status copy"
```

---

### Task 4: Quick Start — uvx-first + install tabs + command audit

**Files:**
- Modify: `docs-site/quick-start.md`
- Modify: `mkdocs.yml` (`markdown_extensions`: add `pymdownx.tabbed`, `pymdownx.details`)

**Interfaces:**
- Consumes: tabbed extension for the install options.

- [ ] **Step 1: Add tab extensions to `mkdocs.yml`** under `markdown_extensions:`
```yaml
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.details
```

- [ ] **Step 2: Verify the real CLI surface before editing**

```bash
python -m pythonlings --help 2>/dev/null || pipx run pythonlings --help 2>/dev/null || true
```
Note the actual subcommands (`init, run, dry-run, hint, list, topics, reset, update, start, watch`). Only document commands that appear in `--help`. If `solution`/`verify` are absent, remove them from the docs.

- [ ] **Step 3: Rewrite `docs-site/quick-start.md`** — lead with `uvx`, alternatives in tabs, audited commands. Key required content:
  - Zero-install: `uvx pythonlings init --path ~/pythonlings-workspace` then `uvx pythonlings`.
  - Install tabs:
    ```markdown
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
    ```
  - Useful commands list using ONLY verified subcommands.
  - Exercise loop paragraph (`# I AM NOT DONE` marker → fix → check → advance).
  - Remove the "After PyPI publishing is enabled…" block and any `@v0.1.0` line.

- [ ] **Step 4: Build + stale-string check**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
grep -riE "v0\.1\.0|PyPI publishing is enabled|@v0\.1\.0" docs-site/quick-start.md
```
Expected: build exit 0; grep prints nothing.

- [ ] **Step 5: Commit**

```bash
git add docs-site/quick-start.md mkdocs.yml
git commit -m "feat(docs): make Quick Start uvx-first with install tabs"
```

---

### Task 5: Interface page — audit commands & keybindings

**Files:**
- Modify: `docs-site/interface.md`

- [ ] **Step 1: Confirm keybindings/commands against the app** — cross-check the F-key table and any commands against `pythonlings/screens/` bindings and `pythonlings --help`. Correct anything stale; add `start`/`watch` if they are user-facing entry points.

- [ ] **Step 2: Edit `docs-site/interface.md`** accordingly (keep the screenshots, which exist). Ensure no command is documented that `--help` does not list.

- [ ] **Step 3: Build**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: exit 0.

- [ ] **Step 4: Commit**

```bash
git add docs-site/interface.md
git commit -m "fix(docs): reconcile interface keybindings and commands with the app"
```

---

### Task 6: Polish remaining pages — roadmap, curriculum, local-docs, contributing

**Files:**
- Modify: `docs-site/roadmap.md`, `docs-site/curriculum.md`, `docs-site/local-docs.md`, `docs-site/contributing.md`

- [ ] **Step 1: Update `roadmap.md`** — move "Finish PyPI publishing" to a "Shipped" section (it's done); reflect `v0.3.1`; keep still-true forward items.

- [ ] **Step 2: Light-polish `curriculum.md` (counts already correct: 292/31), `local-docs.md`, `contributing.md`** — fix any `pylings`→`pythonlings` drift and any stale install/version copy.

- [ ] **Step 3: Build + sitewide stale-string check**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
grep -riE "v0\.1\.0|reserved for PyPI|PyPI release is live|@v0\.1\.0|python-learnings" docs-site/
```
Expected: build exit 0; grep prints nothing.

- [ ] **Step 4: Commit**

```bash
git add docs-site/roadmap.md docs-site/curriculum.md docs-site/local-docs.md docs-site/contributing.md
git commit -m "docs: refresh roadmap and polish remaining pages"
```

---

### Task 7: New page — How It Works

**Files:**
- Create: `docs-site/how-it-works.md`
- Modify: `mkdocs.yml` (`nav`)

- [ ] **Step 1: Write `docs-site/how-it-works.md`** covering: the edit→check→advance loop; the `# I AM NOT DONE` marker and why removing it is required; a worked broken→fixed→green example (a `variables`-style snippet); where progress is stored (`<workspace>/.pythonlings/state.json`, atomic writes with `.bak`); embed the demo GIF.

- [ ] **Step 2: Add to `nav`** in the correct position (after Quick Start — see Task 9 for full order):
```yaml
  - How It Works: how-it-works.md
```

- [ ] **Step 3: Build (strict catches an orphaned page)**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: exit 0.

- [ ] **Step 4: Commit**

```bash
git add docs-site/how-it-works.md mkdocs.yml
git commit -m "docs: add How It Works walkthrough page"
```

---

### Task 8: New page — FAQ

**Files:**
- Create: `docs-site/faq.md`
- Modify: `mkdocs.yml` (`nav`)

- [ ] **Step 1: Write `docs-site/faq.md`** answering: How is this different from Rustlings? Do I need `uv`? Which Python versions (3.9+)? Where is my progress stored? How do I update / reset? Does it work offline? Is it on PyPI? Keep answers short and accurate (uvx-first, `v0.3.1`).

- [ ] **Step 2: Add to `nav`** (after Local Docs — see Task 9):
```yaml
  - FAQ: faq.md
```

- [ ] **Step 3: Build**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: exit 0.

- [ ] **Step 4: Commit**

```bash
git add docs-site/faq.md mkdocs.yml
git commit -m "docs: add FAQ page"
```

---

### Task 9: Final navigation order

**Files:**
- Modify: `mkdocs.yml` (`nav`)

- [ ] **Step 1: Set the final `nav` block**
```yaml
nav:
  - Home: index.md
  - Quick Start: quick-start.md
  - How It Works: how-it-works.md
  - Interface: interface.md
  - Curriculum: curriculum.md
  - Local Docs: local-docs.md
  - FAQ: faq.md
  - Contributing: contributing.md
  - Roadmap: roadmap.md
```

- [ ] **Step 2: Build (strict verifies every nav target exists and nothing is orphaned)**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: exit 0.

- [ ] **Step 3: Commit**

```bash
git add mkdocs.yml
git commit -m "docs: order navigation for a first-timer path"
```

---

### Task 10: Social-share cards + CI imaging deps

**Files:**
- Modify: `requirements-docs.txt`
- Modify: `mkdocs.yml` (`plugins`, `extra.social`, `copyright`)
- Modify: `.github/workflows/pages.yml`

**Interfaces:**
- Produces: per-page OG images at build time **in CI only** (gated by the `CI` env var) so local builds don't require system imaging libraries.

- [ ] **Step 1: Update `requirements-docs.txt`**
```
mkdocs-material[imaging]>=9.5
```

- [ ] **Step 2: Add the `social` plugin (CI-gated), social links, and copyright to `mkdocs.yml`**
```yaml
plugins:
  - search
  - social:
      enabled: !ENV [CI, false]

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/abhiksark/pythonlings
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/pythonlings/

copyright: Copyright &copy; 2026 Pythonlings · MIT License
```

- [ ] **Step 3: Add imaging system deps + `CI` env to `.github/workflows/pages.yml`** — in the `build` job, before `mkdocs build --strict`, add a step:
```yaml
      - name: Install social-card system deps
        run: sudo apt-get update && sudo apt-get install -y libcairo2-dev libfreetype6-dev libffi-dev libjpeg-dev libpng-dev libz-dev pango1.0-tools
```
And ensure the build step runs with `CI: "true"` (GitHub Actions sets `CI=true` automatically, which satisfies the `!ENV [CI, false]` gate).

- [ ] **Step 4: Verify local build still passes (social disabled locally)**

```bash
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: exit 0 (the `social` plugin is disabled because `CI` is unset locally). Re-read `pages.yml` to confirm the deps step precedes the build step.

- [ ] **Step 5: Commit**

```bash
git add requirements-docs.txt mkdocs.yml .github/workflows/pages.yml
git commit -m "feat(docs): add social-share cards built in CI"
```

---

### Task 11: Final verification sweep

**Files:** none (verification only; fix-forward commits if needed)

- [ ] **Step 1: Strict build is clean**

```bash
source .venv-docs/bin/activate
mkdocs build --strict --site-dir /tmp/pl-site
```
Expected: exit 0, zero warnings.

- [ ] **Step 2: No stale strings anywhere in the site**

```bash
grep -riE "v0\.1\.0|reserved for PyPI|PyPI release is live|@v0\.1\.0|python-learnings|\bpylings\b" docs-site/ mkdocs.yml
```
Expected: nothing (the only allowed mention of `pylings` is none in docs-site copy).

- [ ] **Step 3: Install commands match the README; CLI references match `--help`**

```bash
grep -riE "uvx pythonlings|pipx install pythonlings|uv tool install pythonlings|pip install pythonlings" docs-site/ | head
```
Confirm the canonical `uvx pythonlings` appears and no GitHub-tag install remains.

- [ ] **Step 4: Manual preview**

```bash
mkdocs serve
```
Confirm in the browser: hero renders centered with the demo GIF; dark-mode toggle works; logo + favicon show; nav order matches Task 9; How It Works and FAQ pages load.

- [ ] **Step 5 (optional): Confirm social cards build in a CI-like run** (only if local cairo/pango available)

```bash
CI=true mkdocs build --strict --site-dir /tmp/pl-site-ci
```
Expected: exit 0 with `social` generating images; if local system libs are missing, skip and rely on the CI workflow.

- [ ] **Step 6: Commit any fixes** (if Steps 1–4 surfaced issues)

```bash
git add -A && git commit -m "docs: final verification fixes for site overhaul"
```

---

## Self-review

- **Spec coverage:** Theme/palette/dark mode (T1), logo/favicon (T2), hero + index accuracy (T3), quick-start uvx-first + tabs (T4), interface audit (T5), roadmap/remaining polish (T6), How It Works (T7), FAQ (T8), nav reorder (T9), social cards + CI (T10), verification incl. strict build + grep gates (T11). All spec sections map to a task.
- **Placeholder scan:** config/CSS/SVG/HTML shown in full where it is "code"; prose pages (How It Works, FAQ) are specified by required content + accuracy constraints rather than full final prose, which the implementer writes from the verified facts in Global Constraints.
- **Type/name consistency:** hero classes defined in T1 `extra.css` (`.pl-hero`, `.pl-eyebrow`, `.pl-title`, `.pl-subtitle`, `.pl-install`, `.pl-ctas`, `.pl-btn`, `.pl-btn--ghost`, `.pl-stats`) are exactly the classes used by `index.md` in T3. `assets/logo.svg`/`assets/favicon.svg` referenced in T1/T2 match the created files. Nav entries added in T7/T8 match the final order in T9.
