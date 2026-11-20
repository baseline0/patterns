# Cache-aside trades consistency for latency

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Statement**: Cache-aside reduces read latency and backend load by serving hot data from a cache, at the cost of staleness, invalidation complexity, and failure modes.

**Invariant**: A cache entry is treated as an optimization: the source of truth remains authoritative, and correctness depends on an explicit freshness or invalidation policy.

## Steps

- **Fast-path cache lookup**: On a read, the application probes the cache first; a hash-based cache makes membership/lookup constant time on average, so hits avoid the slower source-of-truth path.
- **Miss populates cache** (depends on lookup): On a miss, the application reads from the source of truth and writes the result into the cache for subsequent reads.
- **Freshness is bounded by policy** (depends on miss-fill): Because updates may bypass or race the cache, entries can become stale until TTL expiry or explicit invalidation; stronger consistency requires tighter coordination and higher write cost.
- **Operational trade-offs surface** (depends on lookup, staleness): Benefits (lower latency, reduced load) trade against cold-start misses, stampedes on expiry, cache eviction, and extra invalidation logic that increases system complexity.

**Complexity**: O(1) average cache lookup on hits; end-to-end read cost becomes source-of-truth cost on misses plus invalidation/coordination overhead on writes.

## Explore

- Open in explorer: `../../site/index.html#proofs:proof:cache-aside-tradeoffs` (`just -f site/justfile serve`)

## Linked claims

- `dict-lookup-is-constant-time`
