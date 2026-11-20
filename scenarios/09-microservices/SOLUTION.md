# SOLUTION: Microservices order system

## Model solution

Define four services by business capability: order, payment, inventory, and shipping. Each owns its database and exposes events or commands through a broker. An orchestrated saga drives order placement through reserve stock, authorize payment, and create shipment, with compensating actions for each failure. Per-downstream bulkheads and circuit breakers isolate latency and failures; all steps are idempotent and correlated.

Provider mapping, using generic names elsewhere: AWS uses containers on a managed runtime, queues or event buses, and per-service stores; Azure uses Container Apps or AKS, Service Bus, and per-service data stores; GCP uses Cloud Run or GKE, Pub/Sub, and per-service databases.

## Rationale

- Business-capability boundaries let teams change internals independently.
- Data ownership stops coupling through shared tables and cross-service joins.
- A saga provides explicit consistency and compensation without a distributed transaction.
- Orchestration gives one place to see saga state, enforce timeouts, and trigger compensation.
- Idempotent steps and correlation IDs make retries and tracing safe.
- Bulkheads and circuit breakers prevent one slow dependency from taking down the order path.

## Architecture

```
API gateway -> Order service (owns order DB)
                  | command/event: reserve stock -> Inventory service (owns stock DB)
                  | command/event: authorize payment -> Payment service (owns payment DB)
                  | command/event: create shipment -> Shipping service (owns shipment DB)
                  |
                  `-> saga state: pending -> stocked -> paid -> shipped
                                   |-> timeout -> compensate in reverse order
                                   `-> failure -> release stock / void authorization / cancel shipment

Per downstream call: timeout + jittered retry + bulkhead pool + circuit breaker
Cross-cutting: correlation ID, contract tests, saga state metrics
```

## Trade-offs

- Choreography is loosely coupled but harder to observe; orchestration is visible but adds a coordinator dependency.
- Events scale decoupling but make user-facing consistency eventual.
- Fine-grained services increase autonomy but add deployment and debugging overhead.
- Compensation logic must be maintained alongside every forward step.
- Circuit breakers reduce cascade failure but can cause false outages if thresholds are too sensitive.
- Bulkheads waste reserved capacity during normal operation to protect failures.

## Failure modes

- Saga stuck in an intermediate state because no timeout or compensating action exists.
- Compensation not idempotent, so a retry releases stock twice.
- Shared database reintroduces coupling and blocks independent schema changes.
- Retry storm against a down payment service exhausts shared threads.
- Circuit breaker never probes recovery or opens on benign latency spikes.
- Bulkhead too small causes self-inflicted failures under normal peak load.
- Missing correlation ID makes cross-service tracing impossible.
- Contract change breaks consumers without a failing test.

## Local validation only

- Use the emulator to run the happy path and confirm the saga reaches shipped.
- Simulate a payment decline and confirm compensation releases stock and cancels or voids prior steps.
- Simulate a payment timeout and confirm the circuit opens after the configured threshold and a half-open probe is attempted.
- Replay a duplicate saga step and confirm no double charge or double stock release.
- Confirm in notes that no service reads another service's table.
- Run `terraform plan` and verify per-service topics, subscriptions, identities, and data resources; check timeout/retry policy values in configuration review.
- Do not call real payment systems, start a real cluster, or create cloud databases.

## Note

Eventual consistency is acceptable only if the user is told the truth about order state. Do not show confirmed success before the saga reaches a confirmed state.
