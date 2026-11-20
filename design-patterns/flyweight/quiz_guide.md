# Quiz: Flyweight

> Generated from `content/`.

## 1. Flyweight saves memory by:

A. Compressing objects on disk
B. Sharing intrinsic state and externalizing extrinsic state
C. Using lazy database queries
D. Batching network calls

**Answer: B.** Common immutable data is stored once and reused across many logical instances.

## 2. A precondition for safe Flyweight use is:

A. Intrinsic state must be mutable by clients
B. Clear separation between shared and per-use state
C. All objects must live in one process globally
D. No factory can be used

**Answer: B.** Shared state must be immutable or carefully controlled; extrinsic state is supplied per operation.
