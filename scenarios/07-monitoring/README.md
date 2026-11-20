# README: Observability and incident response

## Learning objective

Design an observability and incident-response practice around user-visible SLOs, RED and USE metrics, correlated logs and traces, manageable alerts, and a closed incident loop.

## Scenario story

Checkout latency is intermittent. The dashboard shows green CPU, the on-call engineer has nine duplicate alerts, and no one can tell whether the slowdown started at the gateway, a downstream call, or the database. The team wants a design that answers those questions during the incident and prevents the same gap next time.

## Constraints

- Use generic observability terms. If you name provider services, name all three: AWS, Azure, and GCP.
- No live paging, real user data, or cloud agent installation.
- Local emulator and `terraform plan` only; synthetic requests are allowed locally.
- Define SLOs before alerts; do not start from a list of host thresholds.
- Work within a 30-60 minute drill.

## Success criteria

- At least one user-facing SLO with an error budget is defined.
- RED metrics cover request-driven services and USE metrics cover resources.
- Logs are structured and share a correlation ID with traces.
- Alerts are symptom-based, owned, deduplicated, and linked to a runbook.
- An incident loop from detection to follow-up action is described.
- Validation uses synthetic local traffic, emulator inspection, and `terraform plan` only.

## Plan-only / cost-free boundary

Write SLOs, metric names, log fields, alert rules, and runbook notes locally. Generate synthetic requests against the local emulator where supported. Use `terraform plan` to review alert and dashboard definitions. Do not connect to real paging, ingest real customer data, or install production agents.

## Starter structure

```
scenarios/07-monitoring/
  README.md
  HINTS.md
  SOLUTION.md
  RUBRIC.md
  plan/
    slos.md
    alerts.md
    runbooks/
  dashboards/
  alerts/
```

Sketch these paths in notes; only the four committed documents are required for the drill.

## Exercise (30-60 minutes)

- 0-10 min: Write one availability and one latency SLO for checkout.
- 10-20 min: Map RED and USE metrics to the critical path.
- 20-35 min: Define log fields, trace spans, and correlation IDs.
- 35-45 min: Design burn-rate alerts, ownership, and suppression rules.
- 45-55 min: Walk the incident loop including review and follow-up actions.
- 55-60 min: List local synthetic and plan evidence; self-score with the rubric.
