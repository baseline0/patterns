# ADR 0003: Keep provider details in mappings and plan-only fixtures

**Status:** ACCEPTED
**Date:** 2026-11-20
**Deciders:** Mark Alexiuk

## Context

The repository promises vendor-agnostic patterns with AWS, Azure, and GCP implementations. Existing Terraform examples were
AWS-only scenario scripts, and `terraform/aws`, `terraform/azure`, and `terraform/gcp` were empty.

## Options

1. Write three full provider tutorials per pattern and run live deployments in exercises.
2. Keep the pattern as the unit of learning, map it to each provider in YAML, and provide minimal plan-only fixtures.
3. Defer provider mappings until every scenario has a live multi-cloud stack.

## Decision

Option 2. `providers/content/*.yaml` is the source of truth for provider service mappings. Each mapping names a fixture
under `terraform/<provider>/<pattern>/`; fixtures support `init`, `validate`, and `plan` only.

## Consequences

- Learning stays cost-free and vendor-agnostic.
- Provider drift is visible in one generated matrix and in quiz cards.
- Fixtures cannot exercise live IAM or stateful behaviour; those are documented as limitations, not hidden.
