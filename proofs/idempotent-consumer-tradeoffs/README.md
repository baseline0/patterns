# Idempotent consumers trade storage for safe retries

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Statement**: Making message consumers idempotent allows at-least-once delivery and retries without duplicate side effects, at the cost of deduplication state, retention policy, and coordination.

**Invariant**: For a given idempotency key, applying the same operation more than once produces the same externally visible result as applying it once.

## Steps

- **Identify operations uniquely**: Each message or request carries a stable idempotency key so repeated deliveries can be recognized as the same logical operation.
- **Check-before-apply** (depends on dedupe-key): The consumer tests whether the key was already processed; constant-time hash lookups or set membership checks avoid linear scans as processed history grows.
- **Record effect atomically enough** (depends on seen-check): On first application the consumer persists the result or marks the key seen so subsequent retries take the no-op/return-prior-result path.
- **Safety gained, state and lifecycle added** (depends on record, seen-check): Retries become safe under redelivery and crashes, but the system must store, expire, and sometimes distribute dedupe state, and define behavior when keys collide or state is lost.

**Complexity**: O(1) average deduplication check/record per message plus storage proportional to retained keys; enables correctness under at-least-once delivery.

## Explore

- Open in explorer: `../../site/index.html#proofs:proof:idempotent-consumer-tradeoffs` (`just -f site/justfile serve`)

## Linked claims

- `set-membership-beats-list-search`
- `dict-lookup-is-constant-time`
