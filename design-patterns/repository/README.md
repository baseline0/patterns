# Repository

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: application

**Intent**: Mediate between domain and data mapping layers through a collection-like interface for aggregates.

## Problem

Domain logic becomes coupled to queries, ORM APIs, and persistence details, making it hard to test and evolve.

## Structure

```text
Domain/Service -> Repository interface
Repository -> Data Mapper/ORM/DB
Repository returns domain aggregates, not rows/clients
```

## Participants

- **Repository interface**: Declares collection-oriented access methods for aggregates.
- **ConcreteRepository**: Implements persistence using a data store or ORM.
- **Domain aggregate**: Business object managed and returned by the repository.

## Forces

- Domain model should be persistence-ignorant.
- Query and storage technologies may change.
- Testing needs in-memory substitutes.

## Consequences

- **Benefit**: Improves separation of concerns and testability of domain logic.
- **Cost**: Can hide important query capabilities or add leaky abstractions if over-generalized.

## Smells

- Fixed: Domain services issuing raw SQL/ORM calls directly, Duplicated query construction across use cases
- Created: Generic repositories that obscure intentful queries, Anemic interfaces that leak persistence concerns

## Python sketch

```python
class UserRepo:
    def __init__(self):
        self._db = {}

    def add(self, user: dict):
        self._db[user["id"]] = user

    def get(self, user_id: int):
        return self._db.get(user_id)

repo = UserRepo()
repo.add({"id": 1, "name": "A"})
print(repo.get(1))
```

## Interview example

A layered CRUD API (04-crud-api) uses repositories so handlers and domain services depend on aggregate operations rather than database clients.

## Related architecture patterns

- `04-crud-api`
- `layered`
- `cqrs`
