# README: Safe multi-environment CI/CD pipeline

## Learning objective

Design a release pipeline that moves one immutable artifact through separate environments with plan-only gates, explicit approvals, a controlled rollout strategy, a tested rollback, and secrets that never enter source control or plan output.

## Scenario story

A checkout service caused a production outage when a rushed release skipped review and overwrote shared state. The team now needs a pipeline that makes safe releases routine: every environment gets its own state, every promotion is reviewed, and a bad release can be reversed without a heroic debugging session.

## Constraints

- Use generic CI/CD terms. If you name provider services, name all three: AWS, Azure, and GCP.
- No live deployment, real credentials, runners, or environments are created.
- `terraform plan` and dry-run pipeline commands only; local emulator use is allowed for dev-like checks.
- One build artifact is promoted unchanged from dev to staging to production.
- Rollback must use a previously known-good artifact, not a hand-edited fix.
- Work within a 30-60 minute drill.

## Success criteria

- Dev, staging, and production have separate state and separate approval boundaries.
- A plan artifact is produced and reviewed before each promotion.
- Blue-green or canary rollout is chosen with a stated traffic split and observation window.
- Rollback trigger, owner, and target version are explicit.
- Secrets come from a secret manager or ephemeral injection and are masked in logs and plan output.
- Evidence comes from dry runs, emulator checks, and `terraform plan` only.

## Plan-only / cost-free boundary

Write pipeline and environment notes locally. Use `terraform plan` for every environment definition and a dry-run form of any pipeline command. Do not connect to a real runner, create environments, store real tokens, or apply to production. Treat `plan` output as a review artifact, not a deployment.

## Starter structure

```
scenarios/06-cicd-pipeline/
  README.md
  HINTS.md
  SOLUTION.md
  RUBRIC.md
  plan/
    environments.md
    pipeline.md
  terraform/
    modules/
    envs/
      dev/
      staging/
      prod/
  policies/
```

Sketch these paths in notes; only the four committed documents are required for the drill.

## Exercise (30-60 minutes)

- 0-10 min: Map environments, state boundaries, and who approves each promotion.
- 10-25 min: Draw pipeline stages and place plan-only gates before approvals.
- 25-40 min: Choose blue-green or canary; define observation window and rollback trigger.
- 40-50 min: Define secret sources, masking rules, and audit records.
- 50-60 min: List emulator/`terraform plan`/dry-run evidence and self-score with the rubric.
