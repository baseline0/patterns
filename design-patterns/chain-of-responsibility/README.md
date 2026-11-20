# Chain of Responsibility

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: behavioral

**Intent**: Pass a request along a chain of handlers until one handles or processes it.

## Problem

Coupling senders to specific handlers or writing large conditional dispatch logic makes request processing rigid.

## Structure

```text
Client -> Handler.handle(req)
Handler -> next.handle(req) (optional)
ConcreteHandlerA/B decide to handle or forward
```

## Participants

- **Handler**: Declares handling interface and reference to the next handler.
- **ConcreteHandler**: Handles requests it is responsible for or forwards them.
- **Client**: Submits requests to the chain entry point.

## Forces

- More than one object may handle a request.
- Handler set or order may vary.
- Sender should not know the concrete handler.

## Consequences

- **Benefit**: Decouples senders from receivers and makes pipelines of checks or transforms composable.
- **Cost**: A request may go unhandled and chains can be harder to trace.

## Smells

- Fixed: Large conditional dispatch blocks, Tight coupling between request emitters and processors
- Created: Unclear ownership when no handler acts, Debug difficulty across long chains

## Python sketch

```python
class Handler:
    def __init__(self, nxt=None):
        self.nxt = nxt

    def handle(self, req: dict):
        if self.nxt:
            return self.nxt.handle(req)
        return None

class Auth(Handler):
    def handle(self, req: dict):
        if not req.get("user"):
            return "401"
        return super().handle(req)

class RateLimit(Handler):
    def handle(self, req: dict):
        if req.get("burst"):
            return "429"
        return "200"

chain = Auth(RateLimit())
print(chain.handle({"user": "a", "burst": False}))
```

## Interview example

An API gateway in front of microservices (09-microservices) can run auth, rate-limit, and validation handlers in sequence before forwarding requests.

## Related architecture patterns

- `09-microservices`
- `layered`
- `02-serverless-api`
