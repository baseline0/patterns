# Quiz: Memento

> Generated from `content/`.

## 1. Memento preserves encapsulation by:

A. Making all state public for caretakers
B. Letting the originator create and consume opaque snapshots
C. Storing state only in global variables
D. Serializing directly in every client

**Answer: B.** Caretakers hold snapshots without reading their internal structure.

## 2. In event-driven systems, mementos are often used for:

A. Routing messages between brokers
B. Checkpointing state for recovery/undo scenarios
C. Load balancing HTTP traffic
D. Schema migration

**Answer: B.** Snapshots can complement event streams for rollback or fast restore points.
