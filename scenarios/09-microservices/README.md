# README: Microservices order system

## Learning objective

Design a microservices order system with clear service boundaries and data ownership, a saga for cross-service consistency, and resilience patterns including bulkheads and circuit breakers.

## Scenario story

A monolithic order flow has been split into order, payment, inventory, and shipping teams. Releases now interfere with each other, a slow payment call exhausts every order worker, and a failed shipment leaves orders stuck in a confusing state. The new design must keep teams independent without becoming a distributed monolith.

## Constraints

- Use generic microservice terms. If you name provider services, name all three: AWS, Azure, and GCP.
- No live deployment, real payments, or cloud service provisioning.
- Local emulator and `terraform plan` only; local fault injection in notes is allowed.
- Each service owns its data; no shared tables or cross-service joins.
- Work within a 30-60 minute drill.

## Success criteria

- Service boundaries align to business capabilities with explicit data ownership.
- A saga defines the order-to-shipment sequence and compensating actions.
- Every saga step is idempotent and carries a correlation ID.
- Bulkheads isolate downstream calls so one slow dependency cannot exhaust all capacity.
- Circuit breakers with timeouts and jittered retries fail fast and probe recovery.
- Validation uses emulator fault cases and `terraform plan` only.

## Plan-only / cost-free boundary

Sketch services, databases, topics, and policies locally. Simulate happy path, decline, and timeout cases against a local emulator or in notes. Use `terraform plan` to review topics, permissions, and per-service resources. Do not start containers in a real cluster, call payment providers, or create cloud databases.

## Starter structure

```
scenarios/09-microservices/
  README.md
  HINTS.md
  SOLUTION.md
  RUBRIC.md
  plan/
    boundaries.md
    saga.md
    resilience.md
  contracts/
  terraform/
```

Sketch these paths in notes; only the four committed documents are required for the drill.

## Exercise (30-60 minutes)

- 0-10 min: Draw service boundaries and the data each service owns.
- 10-25 min: Map the saga steps, compensations, and timeouts.
- 25-40 min: Add bulkheads, circuit breakers, retries, and correlation IDs.
- 40-50 min: Define contract tests and failure simulations.
- 50-60 min: List emulator/plan evidence and self-score with the rubric.
