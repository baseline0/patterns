# SOLUTION: Observability and incident response

## Model solution

Define user-facing SLOs for the checkout path with error budgets and burn-rate alerts. Instrument request-driven services with RED metrics and runtime resources with USE metrics. Emit structured logs and traces that share a correlation ID. Route symptom alerts to a named owner with a runbook; suppress duplicates and make non-urgent signals ticket-only. Close every incident with a review and owned follow-up actions.

Provider mapping, using generic names elsewhere: AWS uses CloudWatch metrics, logs, alarms, and X-Ray; Azure uses Monitor, Log Analytics, and Application Insights; GCP uses Cloud Monitoring, Cloud Logging, and Cloud Trace.

## Rationale

- SLOs align alerts with user experience rather than infrastructure vanity metrics.
- Error budgets make reliability trade-offs discussable and measurable.
- RED explains request behavior; USE explains resource constraints behind it.
- Correlation IDs connect logs, traces, and metrics into one investigation path.
- Owned symptom alerts with runbooks reduce fatigue and shorten triage.
- An incident loop turns a one-off fix into a system improvement.

## Architecture

```
User request -> gateway -> service -> store
     |            |          |         |
     |-> metrics: RED per route, USE per runtime
     |-> logs: structured fields + correlation ID
     `-> traces: spans across gateway, service, queue, store
              |
              v
SLO + error budget -> multi-window burn-rate alerts -> owner + runbook
              |
              v
incident: detect -> triage -> mitigate -> communicate -> resolve -> review
              |
              v
action items -> updated alerts, dashboards, tests, or code
```

## Trade-offs

- Tighter SLOs improve experience but constrain release speed and cost.
- High-cardinality metrics aid debugging but increase storage and query cost.
- Full trace sampling gives complete visibility but costs more; head-based sampling can miss rare errors.
- Paging on every anomaly causes fatigue; ticket-only alerts may be missed during real incidents.
- More dashboards help until nobody knows which one is authoritative.

## Failure modes

- Alerts based only on CPU while users see errors.
- No alert owner or stale runbook, so the page starts with confusion.
- Missing correlation ID forces manual log stitching.
- Logs contain secrets or personal data, creating a privacy incident.
- Error budget ignored, so reliability work never competes with features.
- Duplicate alerts from multiple layers page the same responder repeatedly.
- Incident review produces action items with no owner or due date.

## Local validation only

- Generate synthetic local requests and errors against the emulator or local stub.
- Confirm metric names for RED and USE appear and that a correlation ID is present in logs and trace spans.
- Simulate a burn-rate condition locally in notes and check the alert threshold, window, owner, and runbook reference.
- Confirm alert rules deduplicate or suppress the same symptom from multiple layers.
- Run `terraform plan` and verify alert definitions, retention settings, and read-only permissions for dashboards.
- Confirm no real personal data is used and no paging integration is contacted.
- Do not install production agents or create live alert policies.

## Note

An alert without a user symptom, owner, and first action is noise. Remove it or downgrade it to a ticket.
