# Unit of Work

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: application

**Intent**: Track changes to objects during a business transaction and coordinate writing them out as a single unit.

## Problem

Multiple repository operations within one use case can become inconsistent without coordinated commit/rollback boundaries.

## Structure

```text
UnitOfWork -> tracks new/dirty/removed aggregates
UnitOfWork -> commit()/rollback()
Repositories register changes with the UnitOfWork
```

## Participants

- **UnitOfWork**: Maintains change tracking and transaction boundary.
- **Repository**: Registers object changes with the unit of work.
- **Data mapper/session**: Flushes coordinated changes to the persistence store.

## Forces

- A use case spans multiple aggregates or repositories.
- Atomic commit or rollback semantics are required.
- Change tracking should be centralized.

## Consequences

- **Benefit**: Ensures consistency within a transaction and simplifies commit coordination.
- **Cost**: Adds complexity and can be awkward across distributed systems or microservice boundaries.

## Smells

- Fixed: Manual commit/rollback orchestration in every service method, Partial writes when one of several updates fails
- Created: Bloated transaction scopes, Misuse in distributed workflows where local transactions do not apply

## Python sketch

```python
class UnitOfWork:
    def __init__(self):
        self.new = []
        self.committed = False

    def register(self, obj):
        self.new.append(obj)

    def commit(self):
        self.committed = True

    def rollback(self):
        self.new.clear()

uow = UnitOfWork()
uow.register({"id": 1})
uow.commit()
print(uow.committed, len(uow.new))
```

## Interview example

In a 3-tier web app (05-3tier-web), a service-layer unit of work coordinates repository updates so an order and its lines commit or roll back together.

## Related architecture patterns

- `05-3tier-web`
- `layered`
- `saga`
