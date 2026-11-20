# Dependency Injection

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: application

**Intent**: Supply an object’s dependencies from the outside rather than having it construct or locate them internally.

## Problem

Hard-coded dependencies make code difficult to test, configure, and extend across environments.

## Structure

```text
Assembler/Container -> creates dependencies
Assembler -> injects into Client (constructor/setter)
Client depends on abstractions, not concrete construction
```

## Participants

- **Client**: Declares required dependencies through constructor, setter, or parameters.
- **Dependency (abstraction)**: Contract the client relies on.
- **Assembler/Container**: Constructs and wires concrete dependencies into clients.

## Forces

- Implementations vary by environment or test context.
- Clients should follow inversion of control.
- Wiring logic should be centralized and explicit.

## Consequences

- **Benefit**: Improves testability, configurability, and adherence to dependency inversion.
- **Cost**: Can obscure object creation flow and introduce container/configuration complexity.

## Smells

- Fixed: Hard-coded `new` calls deep in business logic, Difficult unit tests requiring heavy patching of internals
- Created: Overly magical containers and hidden wiring, Configuration complexity for simple applications

## Python sketch

```python
class Clock:
    def now(self) -> str: return "real"

class FixedClock:
    def now(self) -> str: return "fixed"

class Service:
    def __init__(self, clock):
        self.clock = clock

    def stamp(self) -> str:
        return self.clock.now()

print(Service(FixedClock()).stamp())
```

## Interview example

In a microservices codebase (09-microservices), dependency injection wires repositories, clients, and config per environment so services remain testable and deployable.

## Related architecture patterns

- `09-microservices`
- `layered`
- `04-crud-api`
