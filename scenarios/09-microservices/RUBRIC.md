# RUBRIC: Microservices order system

## Rubric

| Criterion | Points | Pass | Fail |
|---|---:|---|---|
| Boundaries and data ownership | 4 | Services map to capabilities; each owns its DB; no cross-service table reads or joins. | Shared tables or boundaries drawn around technical layers. |
| Saga and compensation | 4 | Forward steps, compensations, timeouts, saga state, and idempotent step IDs are explicit. | No compensation, no timeout, or distributed transaction assumed. |
| Bulkheads and circuit breakers | 4 | Per-downstream pools/queues, timeouts, jittered retries, breaker thresholds, and half-open probe defined. | Shared pool for all calls or retries without timeouts/backoff. |
| Contracts and observability | 4 | Correlation ID, saga metrics, and consumer-driven contract tests are described. | No correlation, no contract checks, or saga state invisible. |
| Emulator and plan-only validation | 4 | Happy path, decline, timeout, and duplicate-step tests run locally; `terraform plan` checked; no live services. | Validation needs real payments or a live cluster. |

Total: 20 points.
