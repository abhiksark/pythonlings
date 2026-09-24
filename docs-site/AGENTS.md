# docs-site/AGENTS.md

## Scope

This guide applies to `docs-site/**`. The root `AGENTS.md` also applies.
`mkdocs.yml` defines the documentation navigation and theme configuration.

## Documentation Site Workflow

Run documentation commands from the repository root:

```bash
python -m pip install -r requirements-docs.txt
mkdocs build --strict
```

Update the `nav` section in `mkdocs.yml` whenever a page is added, removed, or
renamed. Keep documented commands, keyboard bindings, package versions, and
screenshots synchronized with current product behavior.

Run `mkdocs build --strict` before completing any documentation-site change.
