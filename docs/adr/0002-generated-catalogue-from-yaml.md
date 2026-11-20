# ADR 0002: Generate one canonical architecture catalogue from YAML

**Status:** ACCEPTED
**Date:** 2026-11-20
**Deciders:** Mark Alexiuk

## Context

`README.md`, `LEARNING.md`, `SCENARIOS.md`, `patterns/PATTERNS_INDEX.md`, and `data/patterns.json` each implied a different
pattern canon. Seven advertised pattern documents did not exist, and five scenario directories had no model solution.

## Options

1. Keep each document as an independent source of truth and repair links one at a time.
2. Make `architecture/content/catalogue.yaml` the canonical scenario list, let YAML folders define patterns and tactics,
   and generate indexes and review cards from those sources.
3. Store the catalogue in application code and render it at runtime.

## Decision

Option 2. `architecture/tools/build.py` generates `CATALOGUE.md`, `catalogue.json`, `graph.json`, `glossary.json`, and
`index.html`; `cards/tools/build.py` consumes glossaries; `visual/tools/build.py` renders the graph. Documentation links
point to generated indexes instead of maintaining a second list.

## Consequences

- Adding a pattern or scenario is one YAML change plus a drift-guard build.
- Generated outputs must be committed, and a check recipe detects stale files.
- Runtime code never imports sibling repositories or reads the network.
