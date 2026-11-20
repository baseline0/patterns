# HINTS: Observability and incident response

## Progressive hints

1. Start with a user-visible SLO such as successful checkout requests or p95 latency, not with CPU or disk thresholds.
2. Define the error budget explicitly; it is the allowed amount of bad experience in a window.
3. Prefer multi-window burn-rate alerts for SLOs over a single threshold that flakes.
4. RED means rate, errors, and duration for request-driven services. USE means utilization, saturation, and errors for resources.
5. Use one correlation ID from the gateway through services, queues, and the database call.
6. Emit structured logs with stable fields: timestamp, service, request ID, outcome, and latency. Never log secrets or full personal data.
7. Trace the critical path; sample all errors and a smaller share of successful requests.
8. Alert on symptoms users feel, assign each alert one owner, and link a short runbook with the first three actions.
9. Reduce alert fatigue with deduplication, suppression during known maintenance, and ticket-only routing for non-urgent signals.
10. Close the loop: every incident gets a timeline, contributing factors, and action items with owners.
11. Validate with synthetic local requests and `terraform plan` for alert/dashboard rules; do not page anyone.

## Note

A green CPU dashboard does not prove a healthy checkout. Keep the user SLO and the resource metrics as separate layers.
