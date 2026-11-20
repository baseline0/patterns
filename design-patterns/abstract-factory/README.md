# Abstract Factory

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: creational

**Intent**: Provide an interface for creating families of related objects without specifying concrete classes.

## Problem

A system must produce compatible sets of components (UI widgets, storage clients, drivers) that vary by environment but must work together.

## Structure

```text
Client -> AbstractFactory
AbstractFactory -> createA()/createB()
ConcreteFactory1/2 create ProductA1/B1 and ProductA2/B2 families
```

## Participants

- **AbstractFactory**: Declares creation operations for each product in the family.
- **ConcreteFactory**: Creates a consistent family of concrete products.
- **AbstractProduct**: Defines interfaces for each kind of product.
- **Client**: Uses only abstract interfaces to assemble behavior.

## Forces

- Products must be used in compatible families.
- Environment or vendor changes should not leak into clients.
- Switching families should be a single decision.

## Consequences

- **Benefit**: Enforces consistency among related products and centralizes family selection.
- **Cost**: Adding a new product kind requires changing every factory interface and implementation.

## Smells

- Fixed: Mismatched component combinations across environments, Vendor-specific conditionals spread through client code
- Created: Factory interface explosion as product kinds grow, Rigid hierarchies for simple cases

## Python sketch

```python
from abc import ABC, abstractmethod

class Queue(ABC):
    @abstractmethod
    def publish(self, msg: str) -> str: ...

class Blob(ABC):
    @abstractmethod
    def put(self, name: str) -> str: ...

class AwsQueue(Queue):
    def publish(self, msg: str) -> str: return f"sqs:{msg}"

class AwsBlob(Blob):
    def put(self, name: str) -> str: return f"s3:{name}"

class CloudFactory(ABC):
    @abstractmethod
    def queue(self) -> Queue: ...
    @abstractmethod
    def blob(self) -> Blob: ...

class AwsFactory(CloudFactory):
    def queue(self) -> Queue: return AwsQueue()
    def blob(self) -> Blob: return AwsBlob()
```

## Interview example

A portable event-driven app (03-event-driven) can swap an AWS or Azure factory so queue and blob clients come from the same compatible provider family.

## Related architecture patterns

- `03-event-driven`
- `microservices`
- `layered`
