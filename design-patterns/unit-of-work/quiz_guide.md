# Quiz: Unit of Work

> Generated from `content/`.

## 1. Unit of Work primarily manages:

A. UI rendering state
B. A transactional boundary and tracked changes
C. HTTP routing tables
D. Container orchestration

**Answer: B.** It coordinates what must be committed or rolled back as one unit.

## 2. Across microservices with separate databases, Unit of Work alone:

A. Provides global ACID transactions automatically
B. Is limited to local boundaries; sagas/compensation are needed for cross-service consistency
C. Replaces idempotent consumers
D. Eliminates eventual consistency

**Answer: B.** Distributed systems require additional coordination patterns beyond a local unit of work.
