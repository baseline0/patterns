# Iterator

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: behavioral

**Intent**: Provide a way to access elements of an aggregate sequentially without exposing its representation.

## Problem

Clients need to traverse collections with different internal structures without depending on their concrete storage details.

## Structure

```text
Client -> Iterator.next()/has_next()
Aggregate.create_iterator() -> Iterator
ConcreteIterator walks ConcreteAggregate
```

## Participants

- **Iterator**: Defines traversal operations such as next and completion checks.
- **ConcreteIterator**: Maintains traversal state over a specific aggregate.
- **Aggregate**: Declares an operation to create an iterator.
- **ConcreteAggregate**: Returns an iterator over its internal collection.

## Forces

- Multiple traversal strategies may be needed.
- Internal representation should remain encapsulated.
- Clients want a uniform traversal interface.

## Consequences

- **Benefit**: Simplifies client traversal logic and supports multiple simultaneous traversals.
- **Cost**: Adds objects and can be redundant in languages with rich built-in iteration.

## Smells

- Fixed: Clients coupled to internal indexes or node structures, Duplicated traversal code across collection types
- Created: Iterator invalidation complexity on concurrent mutation, Extra abstraction for trivial collections

## Python sketch

```python
class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __iter__(self):
        cur = self.start
        while cur < self.end:
            yield cur
            cur += 1

for n in Range(3, 6):
    print(n)
```

## Interview example

A streaming ingestion job (08-streaming) can iterate partition offsets through a uniform cursor interface without exposing broker-specific storage details.

## Related architecture patterns

- `08-streaming`
- `pipe-and-filter`
- `layered`
