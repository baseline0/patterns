# State

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: behavioral

**Intent**: Allow an object to alter its behavior when its internal state changes by delegating to state objects.

## Problem

Behavior that depends on lifecycle state leads to large conditional blocks and invalid transitions scattered through methods.

## Structure

```text
Context(state) -> state.handle(context)
State defines behavior per state
ConcreteStateA/B implement transitions and actions
```

## Participants

- **Context**: Maintains current state and delegates behavior to it.
- **State**: Defines the interface for state-specific behavior.
- **ConcreteState**: Implements behavior and transitions for a particular state.

## Forces

- Object behavior varies by explicit lifecycle state.
- Transitions must be controlled and understandable.
- Conditionals on state flags are proliferating.

## Consequences

- **Benefit**: Localizes state-specific behavior and makes transitions explicit.
- **Cost**: Increases number of classes and requires careful transition ownership.

## Smells

- Fixed: Large switch/if blocks keyed by status flags, Invalid or duplicated transition logic
- Created: State class proliferation, Fragmented view of overall lifecycle

## Python sketch

```python
class Draft:
    def publish(self, doc):
        doc.state = Published()
        return "published"

class Published:
    def publish(self, doc):
        return "already-published"

class Document:
    def __init__(self):
        self.state = Draft()

    def publish(self):
        return self.state.publish(self)

d = Document(); print(d.publish()); print(d.publish())
```

## Interview example

In a CI/CD pipeline (06-cicd-pipeline), a deployment object can move through queued, running, succeeded, and failed states with state-specific transition rules.

## Related architecture patterns

- `06-cicd-pipeline`
- `saga`
- `event-driven`
