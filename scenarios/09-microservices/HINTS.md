# HINTS: Microservices order system

## Progressive hints

1. Draw boundaries around business capabilities and the data they own, not around technical layers like controller or repository.
2. If two services need the same table to answer a question, the boundary or the query ownership is wrong.
3. A saga is a sequence of local transactions with compensations, not a distributed transaction spanning four databases.
4. Prefer choreography for simple event flows; use orchestration when you need visible state, timeouts, and retries.
5. Give every saga step an event or command ID and a correlation ID; make handlers idempotent.
6. Define compensation for each forward step: reserve stock, release stock; authorize payment, void authorization; create shipment, cancel shipment.
7. Bulkheads separate connection pools, queues, and worker slots per downstream so payment latency cannot consume all order threads.
8. Circuit breakers fail fast after repeated failures and use a half-open probe to test recovery.
9. Retries need timeouts and jitter; never blindly retry a non-idempotent payment capture.
10. Consumer-driven contract tests detect boundary drift before integration.
11. In the emulator, simulate payment timeout and inventory rejection. Use `terraform plan` to check per-service topics, permissions, and data resources.

## Note

A saga without a timeout or compensation owner is just a long-running failure waiting to happen.
