# Factory Method

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: creational

**Intent**: Let subclasses or hook implementations decide which concrete object to create.

## Problem

A framework needs to create products while allowing extensions to choose concrete types without changing core workflow code.

## Structure

```text
Creator.operation() -> calls factory_method()
Creator.factory_method() -> Product
ConcreteCreator overrides factory_method() -> ConcreteProduct
```

## Participants

- **Product**: Defines the interface of objects the creator produces.
- **Creator**: Declares the factory method and uses products in its workflow.
- **ConcreteCreator**: Overrides creation to return a specific concrete product.

## Forces

- Creation varies by environment or extension point.
- Core workflow must remain stable.
- Callers should depend on abstractions, not concrete classes.

## Consequences

- **Benefit**: Decouples object creation from the high-level algorithm that uses it.
- **Cost**: Introduces subclassing or hook points that can proliferate.

## Smells

- Fixed: Hard-coded constructors inside business workflows, Repeated type selection logic scattered in callers
- Created: Parallel creator hierarchies, Over-abstraction for simple instantiation

## Python sketch

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, msg: str) -> str: ...

class Email(Notifier):
    def send(self, msg: str) -> str:
        return f"email:{msg}"

class Service(ABC):
    def alert(self, msg: str) -> str:
        return self.create_notifier().send(msg)

    @abstractmethod
    def create_notifier(self) -> Notifier: ...

class EmailService(Service):
    def create_notifier(self) -> Notifier:
        return Email()

print(EmailService().alert("build failed"))
```

## Interview example

A CI/CD pipeline template (06-cicd-pipeline) can define a job workflow while letting each project supply the factory method that creates its deployer implementation.

## Related architecture patterns

- `06-cicd-pipeline`
- `layered`
- `microservices`
