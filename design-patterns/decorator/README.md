# Decorator

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: structural

**Intent**: Attach additional responsibilities to an object dynamically by wrapping it.

## Problem

Subclassing to add combinations of behaviors (logging, caching, auth, metrics) causes class explosion and rigid composition.

## Structure

```text
Client -> Component
Decorator wraps Component and implements Component
ConcreteDecorator adds behavior before/after delegate call
```

## Participants

- **Component**: Common interface for core objects and decorators.
- **ConcreteComponent**: The original object receiving added behavior.
- **Decorator**: Base wrapper that forwards to a component.
- **ConcreteDecorator**: Adds specific behavior around delegation.

## Forces

- Behavior combinations should be composed at runtime.
- Core class should remain closed to modification.
- Wrappers must preserve the component interface.

## Consequences

- **Benefit**: Enables flexible, mix-and-match behavior without subclass explosions.
- **Cost**: Many small wrappers can complicate debugging and object identity.

## Smells

- Fixed: Subclass explosion for feature combinations, Core classes cluttered with orthogonal concerns
- Created: Deep wrapper chains that are hard to trace, Order-dependent decorator behavior

## Python sketch

```python
class Handler:
    def handle(self, req: dict) -> dict:
        raise NotImplementedError

class Core(Handler):
    def handle(self, req: dict) -> dict:
        return {"ok": True, "id": req["id"]}

class Logging(Handler):
    def __init__(self, inner: Handler):
        self.inner = inner

    def handle(self, req: dict) -> dict:
        res = self.inner.handle(req)
        return {**res, "logged": True}

print(Logging(Core()).handle({"id": 7}))
```

## Interview example

In a CRUD API (04-crud-api), decorators can add auth, metrics, and caching around handlers without changing business logic, aligning with layered boundaries.

## Related architecture patterns

- `04-crud-api`
- `layered`
- `cache-aside`
