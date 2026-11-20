# Proxy

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: structural

**Intent**: Provide a surrogate or placeholder that controls access to another object.

## Problem

Direct access to an object is expensive, remote, unsafe, or needs cross-cutting controls like caching or lazy loading.

## Structure

```text
Client -> Subject interface
Proxy implements Subject and references RealSubject
Proxy may add control before/after forwarding
```

## Participants

- **Subject**: Common interface implemented by proxy and real subject.
- **RealSubject**: The actual object providing core functionality.
- **Proxy**: Controls access to the real subject and may add behavior.

## Forces

- Access requires indirection (lazy init, remote, protection, caching).
- Clients should use the same interface as the real object.
- Control logic must be centralized.

## Consequences

- **Benefit**: Adds access control or optimization transparently to clients.
- **Cost**: Introduces latency/complexity and can obscure failure modes of the real subject.

## Smells

- Fixed: Clients handling lazy loading or remote access details directly, Scattered authorization or caching checks around a service
- Created: Hidden network hops or staleness, Debugging confusion between proxy and real object behavior

## Python sketch

```python
class Api:
    def fetch(self, key: str) -> str:
        return f"value:{key}"

class CachedApi:
    def __init__(self, inner: Api):
        self.inner = inner
        self.cache = {}

    def fetch(self, key: str) -> str:
        if key not in self.cache:
            self.cache[key] = self.inner.fetch(key)
        return self.cache[key]

api = CachedApi(Api())
print(api.fetch("a"), api.fetch("a"))
```

## Interview example

A CRUD service (04-crud-api) can use a proxy in front of a repository or remote client to add caching and auth checks, aligning with cache-aside strategies.

## Related architecture patterns

- `04-crud-api`
- `cache-aside`
- `microservices`
