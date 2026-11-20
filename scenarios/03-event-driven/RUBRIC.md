# RUBRIC: Event-driven order ingress

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| Decoupled ingress | 4 | Ingress validates and appends to a durable queue/topic; consumers are invoked asynchronously. | Client waits on synchronous downstream calls or messages are held only in memory. |
| Idempotency and ordering | 4 | Event IDs with atomic dedupe; stable partition key; per-key sequencing is preserved. | Duplicate side effects possible or ordering key is random per event. |
| Retry and dead-letter handling | 4 | Backoff with jitter, attempt limit, DLQ with context, alerting, and replay path are defined. | Infinite retries, no DLQ, or poison messages block the stream. |
| Schema and observability | 4 | Versioned schema plus depth, age, retry, and DLQ metrics with owners. | Unversioned payloads or no backlog/DLQ visibility. |
| Emulator and plan-only validation | 4 | Duplicate, ordering, and DLQ tests run locally; `terraform plan` checks messaging resources; no live publish. | Validation requires live cloud messaging or omits duplicate and DLQ tests. |

Total: 20 points.
