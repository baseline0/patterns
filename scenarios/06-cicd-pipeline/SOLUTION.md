# SOLUTION: Safe multi-environment CI/CD pipeline

## Model solution

One immutable artifact moves through dev, staging, and production. Each environment has separate state and a dedicated deployment identity. Every stage produces a reviewed plan before an approval. Promotion to production uses a canary or blue-green rollout with a defined observation window; a metric breach halts the rollout and reverts to the prior artifact. Secrets come from a managed secret store with short-lived injection and masked logs.

Provider mapping, using generic names elsewhere: AWS uses CodePipeline or equivalent runners, separate state backends, Secrets Manager, and deployment groups; Azure uses pipelines, separate state, Key Vault, and deployment slots; GCP uses Cloud Build or equivalent runners, separate state, Secret Manager, and progressive delivery.

## Rationale

- A promoted artifact preserves test evidence and eliminates environment-specific rebuild drift.
- Separate state and identities prevent cross-environment writes and make approval boundaries enforceable.
- A reviewed plan makes the approval meaningful and exposes replacement or deletion risk.
- Canary or blue-green limits blast radius and gives a fast revert path.
- Rollback to a prior immutable artifact is predictable and auditable.
- Managed secrets with short-lived injection remove long-lived credentials from repos and logs.

## Architecture

```
Commit -> build + unit tests -> signed immutable artifact
   |
   v
plan(dev) -> approval(dev) -> dev emulator checks
   |
   v
plan(staging) -> approval(staging) -> staging rollout (blue-green or canary) -> smoke checks
   |
   v
plan(prod) -> approval(prod) -> canary 5% -> observe -> 25% -> observe -> 100%
                                  |
                                  `-> SLO breach -> halt -> rollback to prior artifact

Secrets: managed secret store -> short-lived injection at runtime -> masked logs
Audit: artifact digest, plan digest, approver, rollout metrics, rollback target
```

## Trade-offs

- Blue-green gives instant switch and revert but runs two full environments briefly.
- Canary exposes fewer users but needs reliable metrics and longer rollout time.
- More approvals reduce accident risk but slow routine releases.
- Separate state improves isolation but adds duplication and drift risk if modules are not shared.
- Short-lived credentials are safer but require more runner configuration.
- Preserving plan artifacts prevents review mismatch but adds storage and retention rules.

## Failure modes

- Plan is regenerated after approval, so the approver reviewed a different change.
- Pipeline uses one shared identity and writes the wrong environment state.
- Rollback relies on a mutable tag that has been overwritten.
- Canary traffic is skewed by routing rules, so metrics are misleading.
- Database migration is not backward compatible, making rollback impossible.
- Secrets appear in plan output, logs, or cached runner artifacts.
- Approval is bypassed during an incident with no audit record.
- Drift in the target environment makes the plan include unexpected replacements.

## Local validation only

- Dry-run the pipeline definition and confirm stage order, approval placement, and plan gates.
- Run `terraform plan` separately for dev, staging, and production notes using distinct state paths and variables.
- Compare plan output for secret-shaped values and confirm none are present.
- Simulate a canary halt in notes by naming the metric, threshold, owner, and rollback target.
- Verify the rollback step points to an immutable artifact digest from a previous successful release.
- Use the emulator only for dev-like checks; do not connect to real runners or cloud environments.
- Do not create real approvals, secrets, environments, or deployments.

## Note

A plan-only gate is a review control. It does not prove the rollout will succeed; the rollout metrics and rollback path provide that evidence.
