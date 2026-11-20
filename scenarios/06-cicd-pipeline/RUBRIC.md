# RUBRIC: Safe multi-environment CI/CD pipeline

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| Environments and promotion | 4 | Dev/staging/prod have separate state and identities; one immutable artifact is promoted unchanged. | Shared state, rebuilt artifacts, or no isolation between environments. |
| Plan gates and approvals | 4 | Reviewed plan precedes each role-bound approval; plan artifact is preserved for the promotion. | Approvals occur before or without a plan, or plan can change unnoticed. |
| Rollout and rollback | 4 | Blue-green or canary is chosen with traffic split, observation window, halt metric, and rollback to prior immutable artifact. | All-at-once release or rollback depends on manual edits or mutable tags. |
| Secrets and audit | 4 | Managed secret store, short-lived injection, masked logs, and records of approver/artifact/plan. | Secrets in repo or plan output, or no audit trail. |
| Plan-only validation | 4 | Dry run plus `terraform plan` per environment provides evidence; no real runner, environment, or deploy. | Validation requires live deployment or omits plan output review. |

Total: 20 points.
