# ADR 0005: Keep catalog and patterns separate, linked by reference

**Status:** ACCEPTED
**Date:** 2026-11-23
**Deciders:** Mark Alexiuk

## Context

`catalog` (L3, private) is the incubator for educational periodic-table-style reference sites: one folder per subject,
with per-folder source inventories and licence terms. `patterns` (L2, public) is the content-and-rendering layer for
reusable engineering patterns, with deterministic builders and drift guards.

The two repos share vocabulary. `catalog` has an `algorithms` folder ("algorithm patterns") and a `game-theory`
scaffold; `patterns` claims game theory as a pattern family "scoped, not yet written" and has its own internal
`site/catalog.json`. Neither repo references the other, and the fleet manifest lists them independently. Left
undecided, agents are likely to copy subject data into pattern pages, or to pull a Python build toolchain into the
data incubator.

## Options

1. Fold `catalog` into `patterns` and render every subject with the same builders.
2. Fold `patterns` into `catalog` and give every subject a site.
3. Keep two repos. `catalog` owns subject facts and provenance; `patterns` owns pattern structure and rendering. Link
   by subject ID (`catalog_refs`) only. Subjects graduate to standalone site repositories (`periodic-table-inspector`
   is the precedent), copying the builder recipe rather than importing it.

## Decision

Option 3. No absorption in either direction.

- Cross-repo linkage is a shallow reference by ID, never a copy of subject data and never an absolute or
  parent-traversing path.
- Runtime and build code in `patterns` never imports, reads or ingests `catalog`.
- Overlapping families are split by ownership: subject taxonomies (including `algorithms` and `game-theory`) stay in
  `catalog`; teachable pattern content (data structures, quiz decks, proof DAGs, scenarios) stays in `patterns`.
- A subject that is ready for publication graduates to its own site repo. The builders here are a template to copy.

## Consequences

- Both READMEs carry the `catalog-boundary: subject-data-vs-pattern-rendering` marker; unit tests bind the docs and
  the code to it.
- `catalog_refs` values are `subject` or `subject/id`, never paths, URLs or file names.
- Adding a subject does not change `patterns`' generated catalogue; adding a pattern does not change `catalog` data.
- Each repo keeps its own gate and publication posture. `catalog` has no Python build; `patterns` keeps the
  no-sibling-import guard.
