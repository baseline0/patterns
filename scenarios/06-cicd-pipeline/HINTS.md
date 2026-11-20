# HINTS: Safe multi-environment CI/CD pipeline

## Progressive hints

1. Build once and promote the same immutable artifact; rebuilding per environment weakens the evidence from earlier stages.
2. Give each environment its own state, variables, and identity. A promotion should not be able to write another environment's state.
3. Put a `terraform plan` gate before every approval. The approver should see exactly what would change.
4. Make approvals role-bound and auditable; a single engineer should not implicitly bypass staging because production is urgent.
5. Choose blue-green when a fast full switch and instant revert matter; choose canary when you want gradual exposure and metric-based promotion.
6. Define the observation window and the metrics that halt a rollout before you draw the happy path.
7. Rollback must select a prior immutable artifact and a known-good configuration version; it should not depend on manual edits.
8. Keep secrets in a secret manager or short-lived injected credentials. Never place values in repo files, environment literals, or plan text.
9. Mask secret-shaped output and restrict who can read pipeline logs.
10. Add a plan-only gate that fails on drift or unexpected resource replacement rather than silently continuing.
11. Use a dry run of the pipeline plus `terraform plan` per environment as evidence; no real runners or cloud environments.

## Note

An approval after a plan is only useful if the plan cannot change between review and promotion. State how you preserve that link.
