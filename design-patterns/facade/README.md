# Facade

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: structural

**Intent**: Provide a simplified interface to a complex subsystem.

## Problem

Clients must orchestrate many subsystem classes and calls, increasing coupling and misuse risk.

## Structure

```text
Client -> Facade.simple_op()
Facade -> SubsystemA / SubsystemB / SubsystemC
Subsystem classes remain available for advanced use
```

## Participants

- **Facade**: Offers coarse-grained operations that coordinate subsystem work.
- **Subsystem classes**: Implement detailed functionality behind the facade.
- **Client**: Uses the facade for common cases instead of subsystem internals.

## Forces

- Subsystem APIs are complex or unstable.
- Most clients need a narrow, common workflow.
- Direct access may still be required for advanced cases.

## Consequences

- **Benefit**: Reduces coupling and makes common use cases easier and safer.
- **Cost**: Can become a god object if it accumulates unrelated responsibilities.

## Smells

- Fixed: Clients orchestrating many low-level calls in sequence, Duplicated subsystem wiring across callers
- Created: Overgrown facade with too many responsibilities, Hidden subsystem capabilities needed by advanced clients

## Python sketch

```python
class Encoder:
    def encode(self, data: bytes) -> bytes: return data[::-1]

class Storage:
    def save(self, name: str, data: bytes) -> str: return f"stored:{name}:{len(data)}"

class Notifier:
    def notify(self, name: str) -> str: return f"notified:{name}"

class MediaFacade:
    def __init__(self):
        self.encoder = Encoder()
        self.storage = Storage()
        self.notifier = Notifier()

    def publish(self, name: str, data: bytes) -> dict:
        blob = self.encoder.encode(data)
        loc = self.storage.save(name, blob)
        msg = self.notifier.notify(name)
        return {"location": loc, "message": msg}

print(MediaFacade().publish("a.txt", b"hi"))
```

## Interview example

A serverless API (02-serverless-api) can expose a facade over auth, storage, and queue clients so handlers invoke one workflow instead of managing each SDK call.

## Related architecture patterns

- `02-serverless-api`
- `layered`
- `microservices`
