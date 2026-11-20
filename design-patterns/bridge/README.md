# Bridge

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: structural

**Intent**: Decouple an abstraction from its implementation so both can vary independently.

## Problem

Combining multiple abstractions with multiple implementations via inheritance causes class explosion and tight coupling.

## Structure

```text
Abstraction -> Implementor.operation_impl()
RefinedAbstraction extends Abstraction
ConcreteImplementorA/B implement Implementor
```

## Participants

- **Abstraction**: Defines high-level control logic and holds a reference to an implementor.
- **RefinedAbstraction**: Extends the abstraction without changing implementors.
- **Implementor**: Declares low-level operations used by the abstraction.
- **ConcreteImplementor**: Provides a specific implementation of the low-level operations.

## Forces

- Abstraction and implementation dimensions vary independently.
- Inheritance combinations are multiplying.
- Runtime selection of implementation is needed.

## Consequences

- **Benefit**: Reduces subclass explosion and enables independent evolution of both hierarchies.
- **Cost**: Increases design complexity and requires up-front separation of concerns.

## Smells

- Fixed: Cartesian-product inheritance hierarchies, Abstractions hard-wired to one platform implementation
- Created: Extra indirection for simple cases, Unclear split between abstraction and implementation responsibilities

## Python sketch

```python
class Renderer:
    def draw(self, text: str) -> str:
        raise NotImplementedError

class Html(Renderer):
    def draw(self, text: str) -> str:
        return f"<p>{text}</p>"

class Plain(Renderer):
    def draw(self, text: str) -> str:
        return text

class Notification:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    def send(self, text: str) -> str:
        return self.renderer.draw(text)

print(Notification(Html()).send("deploy ok"))
```

## Interview example

A monitoring dashboard (07-monitoring) can separate alert abstractions from delivery implementations (email, chat, pager) so new channels do not require new alert subclasses.

## Related architecture patterns

- `07-monitoring`
- `layered`
- `microservices`
