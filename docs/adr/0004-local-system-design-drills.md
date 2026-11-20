# ADR 0004: Add deterministic system-design drills without runtime content imports

**Status:** ACCEPTED
**Date:** 2026-11-20
**Deciders:** Mark Alexiuk

## Context

Scenario prompts existed, but there was no consistent model solution or rubric, no architecture-style vocabulary, and no
ATAM or ADR practice. The repository must not acquire network, PDF, indexing, or sibling-repository runtime dependencies.

## Options

1. Add a web app that fetches prompts from a service and calls another repository for analysis.
2. Add local CLI drills that read committed YAML and Markdown only.
3. Put all drill text in Python source and skip YAML schemas.

## Decision

Option 2. `scenarios/tools/drill.py`, `quality/tools/atam.py`, and `decisions/tools/adr_coach.py` read repository content
through small loaders. Sources stay in YAML or Markdown, outputs stay deterministic, and local notes are gitignored.

## Consequences

- Drills work offline and can be guarded by unit tests.
- Content authors use schemas instead of editing Python.
- Interactive drills are practice aids; the committed glossary and rubric files remain the reviewable source material.
