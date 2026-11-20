# Quiz: Builder

> Generated from `content/`.

## 1. Builder is a better fit than many constructor parameters when:

A. Objects must be globally unique
B. Construction is stepwise with optional parts and validation
C. Behavior must be swapped at runtime
D. Access to a remote service must be proxied

**Answer: B.** It makes complex, ordered assembly explicit and safe.

## 2. What does a Director contribute?

A. Stores the final product for all clients
B. Encapsulates a reusable construction sequence
C. Selects concrete classes by string name
D. Handles persistence transactions

**Answer: B.** The Director knows the order of steps; builders know how to perform each step.
