# Quiz: Observer

> Generated from `content/`.

## 1. Observer is best characterized as:

A. One-to-one synchronous call chains only
B. A publish/subscribe dependency between subject and observers
C. A data partitioning strategy
D. A compile-time code generator

**Answer: B.** Observers register interest and receive updates when the subject changes.

## 2. In distributed event-driven systems, a common observer risk is:

A. No way to add subscribers
B. Uncontrolled cascades and unclear delivery/ordering semantics
C. Guaranteed global transactions
D. Static schemas only

**Answer: B.** Loose coupling is powerful but requires attention to ordering, retries, and idempotency.
