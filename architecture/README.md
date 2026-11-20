# Architecture catalogue

- **Explore in local catalogue:** run `just -f site/justfile serve` and open `site/index.html` (searchable, cross-linked).

Canonical index for architecture styles, tactics, quality attributes, and scenario exercises. `content/catalogue.yaml`
defines the scenario ladder; the YAML folders define patterns. `tools/build.py` renders `CATALOGUE.md`, `catalogue.json`,
`graph.json`, `glossary.json`, and `index.html`.

## Source folders

- `content/styles/` — architecture styles and structural decisions.
- `content/tactics/` — concrete reliability, scalability, and operability tactics.
- `content/quality-attributes/` — measurable quality-attribute scenarios.
- `content/catalogue.yaml` — the canonical scenario list and its required solution/rubric paths.

## Commands

```bash
just -f architecture/justfile build
just -f architecture/justfile check
just -f architecture/justfile list
```

The generated `glossary.json` joins `cards/deck.json`; `graph.json` feeds the visual architecture page.
