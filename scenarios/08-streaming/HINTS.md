# HINTS: Clickstream streaming pipeline

## Progressive hints

1. Put an append-only log or topic at ingestion; producers should not call processors directly.
2. Partition by a stable key such as session ID or tenant ID. State that ordering is guaranteed per key, not globally.
3. Use event time for click windows and define how late events are handled with a watermark plus allowed lateness.
4. Choose tumbling windows for fixed counts and session windows for inactivity-based behavior.
5. Make aggregates recomputable: raw events are the source of truth, derived views are disposable.
6. Backpressure should be visible as consumer lag. Scale consumers, bound buffers, and define when to sample or shed low-priority events.
7. A hot partition from one popular key needs a mitigation such as salting plus a second-stage aggregation; adding consumers alone will not fix it.
8. Replay must not duplicate sink rows. Use event IDs and idempotent upserts into the analytics store.
9. Schema evolution: adding optional fields with defaults is usually compatible; renaming or changing types in place is breaking.
10. Register versions and check compatibility before producers deploy new shapes.
11. Use the emulator for duplicate and out-of-order synthetic events; use `terraform plan` for retention, partitions, and permissions.

## Note

Exactly-once claims vary by platform. Design the sink write to be idempotent so correctness does not depend on a provider slogan.
