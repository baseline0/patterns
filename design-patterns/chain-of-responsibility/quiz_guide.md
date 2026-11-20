# Quiz: Chain of Responsibility

> Generated from `content/`.

## 1. Chain of Responsibility lets you:

A. Guarantee exactly one handler always runs
B. Decouple sender from the concrete receiver by forwarding along handlers
C. Replicate state across nodes
D. Compile queries into SQL

**Answer: B.** Handlers are linked and each decides whether to act or pass along.

## 2. A risk to manage in handler chains is:

A. Mandatory global locks
B. Requests falling off the end unhandled
C. Inability to add new handlers
D. Loss of type safety in all languages

**Answer: B.** Without a terminal handler or contract, some requests may not be processed.
