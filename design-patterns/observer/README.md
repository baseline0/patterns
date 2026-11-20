# Observer

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: behavioral

**Intent**: Define a one-to-many dependency so dependents are notified when a subject changes state.

## Problem

Components need to react to state changes without hard-coded polling or tight coupling between publisher and subscribers.

## Structure

```text
Subject.attach(observer)
Subject.notify() -> Observer.update(event)
ConcreteObservers react independently
```

## Participants

- **Subject**: Maintains observer list and emits notifications on change.
- **Observer**: Declares the update interface for receiving events.
- **ConcreteObserver**: Reacts to notifications with specific behavior.

## Forces

- Multiple consumers react to the same state change.
- Publisher should not know concrete subscribers.
- Subscription set can change at runtime.

## Consequences

- **Benefit**: Enables loose coupling and dynamic subscription for change propagation.
- **Cost**: Notification order, storms, and debugging event flows can be challenging.

## Smells

- Fixed: Manual polling loops for state changes, Publishers tightly coupled to specific downstream actions
- Created: Hidden cascading updates, Hard-to-trace event chains

## Python sketch

```python
class Subject:
    def __init__(self):
        self._subs = []

    def subscribe(self, fn):
        self._subs.append(fn)

    def publish(self, value):
        for fn in self._subs:
            fn(value)

bus = Subject()
bus.subscribe(lambda v: print("audit", v))
bus.subscribe(lambda v: print("metrics", v))
bus.publish("order-created")
```

## Interview example

An event-driven architecture (03-event-driven) uses observer-like subscriptions so independent consumers react to domain events without coupling to the producer.

## Related architecture patterns

- `03-event-driven`
- `event-driven`
- `08-streaming`
