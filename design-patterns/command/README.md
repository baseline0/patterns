# Command

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: behavioral

**Intent**: Encapsulate a request as an object, allowing parameterization, queuing, logging, and undo.

## Problem

Invokers are tightly coupled to concrete operations, making it hard to queue, audit, retry, or reverse actions.

## Structure

```text
Invoker -> Command.execute()
ConcreteCommand holds Receiver and parameters
Receiver performs the actual work
```

## Participants

- **Command**: Declares an execution interface for an action.
- **ConcreteCommand**: Binds a receiver and parameters to implement the action.
- **Invoker**: Triggers commands without knowing operation details.
- **Receiver**: Contains the business logic needed to fulfill the request.

## Forces

- Actions must be queued, logged, or retried.
- Invoker should be decoupled from operation details.
- Undo/redo or audit trails may be required.

## Consequences

- **Benefit**: Decouples invocation from execution and enables scheduling, auditing, and reversal.
- **Cost**: Introduces many small command objects and lifecycle management concerns.

## Smells

- Fixed: Invokers calling many concrete operations directly, No uniform way to log, queue, or undo actions
- Created: Command class sprawl, Complexity in command persistence and idempotency

## Python sketch

```python
class Light:
    def on(self): return "on"

class SwitchOn:
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        return self.light.on()

queue = [SwitchOn(Light())]
for cmd in queue:
    print(cmd.execute())
```

## Interview example

In an event-driven system (03-event-driven), commands can be serialized to a queue for asynchronous processing with retries and audit logs, complementing queue-based-load-leveling.

## Related architecture patterns

- `03-event-driven`
- `queue-based-load-leveling`
- `cqrs`
