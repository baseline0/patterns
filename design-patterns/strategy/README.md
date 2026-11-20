# Strategy

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: behavioral

**Intent**: Define interchangeable algorithms behind a stable interface so behavior can vary at runtime.

## Problem

A service needs multiple pricing, routing, or ranking behaviors without scattering conditionals across callers.

## Structure

```text
Client -> Context(strategy)
Context -> Strategy.execute()
ConcreteStrategyA / ConcreteStrategyB implement Strategy
```

## Participants

- **Strategy**: Declares the algorithm interface used by the context.
- **ConcreteStrategy**: Implements one algorithm variant.
- **Context**: Delegates work to the selected strategy and holds shared state.

## Forces

- Behavior must change without modifying callers.
- Variants share inputs but differ in policy.
- Selection may happen per request or tenant.

## Consequences

- **Benefit**: Replaces branching logic with composable, testable policies.
- **Cost**: Adds indirection and requires explicit strategy selection.

## Smells

- Fixed: Long switch statements for behavior selection, Duplicated conditional policy logic
- Created: Too many tiny strategy classes, Selection logic leaking into callers

## Python sketch

```python
from dataclasses import dataclass
from typing import Protocol

class Shipping(Protocol):
    def cost(self, weight: float) -> float: ...

class Standard:
    def cost(self, weight: float) -> float:
        return 5 + weight * 1.2

class Express:
    def cost(self, weight: float) -> float:
        return 12 + weight * 2.0

@dataclass
class QuoteService:
    strategy: Shipping

    def total(self, weight: float) -> float:
        return self.strategy.cost(weight)

print(QuoteService(Express()).total(3.0))
```

## Interview example

In a serverless checkout API (02-serverless-api), a Lambda chooses tax or shipping strategies per region while the handler and API contract stay stable.

## Related architecture patterns

- `02-serverless-api`
- `microservices`
- `layered`
