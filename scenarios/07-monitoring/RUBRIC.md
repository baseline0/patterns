# RUBRIC: Observability and incident response

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| SLOs and error budgets | 4 | User-facing availability/latency SLOs with windows and error budgets; alerts derive from them. | Alerts start from host thresholds with no user outcome. |
| RED and USE instrumentation | 4 | RED for services and USE for resources with named metrics on the critical path. | Only one metric family or metrics unrelated to the user journey. |
| Logs and traces | 4 | Structured logs, stable fields, correlation ID, and trace spans across service boundaries without secrets. | Unstructured logs, no correlation, or sensitive data logged. |
| Alert quality and runbooks | 4 | Symptom alerts, named owners, deduplication/suppression, runbook with first actions, non-urgent signals ticketed. | Duplicate pages, no owner, or no runbook. |
| Incident loop and validation | 4 | Detect-to-review loop with owned action items; synthetic local evidence and `terraform plan`; no live paging. | No follow-up loop or validation requires production data/paging. |

Total: 20 points.
