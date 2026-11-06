# ADR 0001: Add the Circuit Breaker pattern after B2

**Status:** PROPOSED
**Date:** 2026-11-06
**Deciders:** Mark Alexiuk

## Context

`TODO.md:35` says: after B2, decide on Circuit Breaker if feedback is positive, otherwise iterate on existing patterns. The Circuit Breaker page already exists at `patterns/08-circuit-breaker.md`. The feedback round is defined in `TODO.md:22-33`, and `docs/FEEDBACK.md` has not been created (`TODO.md:8`).

## Options

1. Add Circuit Breaker as a new pattern once the feedback round is positive.
2. Iterate on the existing patterns first, and defer Circuit Breaker.

## Owner question

What counts as positive feedback for adding Circuit Breaker after B2?

## Consequences

- Option 1: the pattern set grows, and the feedback criteria must be fixed before the round runs.
- Option 2: the existing patterns get more work before any new pattern is added.
