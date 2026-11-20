# Mediator

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: behavioral

**Intent**: Centralize complex interactions between related objects in a mediator to reduce direct dependencies.

## Problem

Many components reference each other directly, creating tangled communication and fragile change propagation.

## Structure

```text
ColleagueA <-> Mediator <-> ColleagueB
Colleagues notify mediator instead of peers
Mediator coordinates responses
```

## Participants

- **Mediator**: Defines coordination interface for colleagues.
- **ConcreteMediator**: Encapsulates interaction rules between colleagues.
- **Colleague**: Communicates through the mediator rather than directly with peers.

## Forces

- Object interactions are many-to-many and hard to reason about.
- Reuse of components is limited by peer coupling.
- Interaction rules change frequently.

## Consequences

- **Benefit**: Reduces coupling between components and localizes collaboration logic.
- **Cost**: Mediator can grow into a complex central controller.

## Smells

- Fixed: Spaghetti references between peer components, Change ripple effects across tightly coupled objects
- Created: God-mediator with excessive knowledge, Hidden workflows centralized in one place

## Python sketch

```python
class ChatRoom:
    def __init__(self):
        self.users = []

    def register(self, user):
        self.users.append(user)
        user.room = self

    def send(self, sender, msg: str):
        for u in self.users:
            if u is not sender:
                u.receive(msg)

class User:
    def __init__(self, name):
        self.name = name
        self.room = None

    def say(self, msg: str):
        self.room.send(self, msg)

    def receive(self, msg: str):
        pass
```

## Interview example

A microservices orchestration layer (09-microservices) can act as a mediator for UI workflows, coordinating service calls instead of letting clients chat with every service directly.

## Related architecture patterns

- `09-microservices`
- `layered`
- `saga`
