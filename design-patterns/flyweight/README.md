# Flyweight

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: structural

**Intent**: Share common intrinsic state across many fine-grained objects to reduce memory use.

## Problem

Large numbers of similar objects duplicate immutable data, causing high memory overhead.

## Structure

```text
Client -> FlyweightFactory.get(key)
Factory returns shared Flyweight(intrinsic)
Client supplies extrinsic state at use time
```

## Participants

- **Flyweight**: Stores shared intrinsic state and operates on extrinsic state.
- **FlyweightFactory**: Creates and caches flyweights by intrinsic key.
- **Client**: Maintains or computes extrinsic state passed to flyweights.

## Forces

- Many objects share immutable data.
- Memory footprint is a bottleneck.
- Intrinsic and extrinsic state can be separated clearly.

## Consequences

- **Benefit**: Reduces memory and allocation costs for large object populations.
- **Cost**: Adds complexity and may increase CPU cost to manage extrinsic state.

## Smells

- Fixed: Millions of objects duplicating the same immutable fields, High memory churn from identical configuration/state blobs
- Created: Harder-to-follow code due to split state, Shared mutable state bugs if intrinsic data is not truly immutable

## Python sketch

```python
class Icon:
    def __init__(self, name: str):
        self.name = name

    def render(self, x: int, y: int) -> str:
        return f"{self.name}@{x},{y}"

class IconFactory:
    def __init__(self):
        self._pool = {}

    def get(self, name: str) -> Icon:
        if name not in self._pool:
            self._pool[name] = Icon(name)
        return self._pool[name]

factory = IconFactory()
print(factory.get("pin").render(1, 2), factory.get("pin") is factory.get("pin"))
```

## Interview example

A monitoring UI (07-monitoring) can share icon/glyph flyweights across thousands of chart points while passing per-point coordinates as extrinsic state.

## Related architecture patterns

- `07-monitoring`
- `cache-aside`
- `01-static-website`
