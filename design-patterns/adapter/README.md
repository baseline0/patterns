# Adapter

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: structural

**Intent**: Convert the interface of a component into one clients expect so incompatible interfaces can collaborate.

## Problem

Integrating third-party or legacy APIs requires changing client code or duplicating translation logic across the system.

## Structure

```text
Client -> Target interface
Adapter implements Target and wraps Adaptee
Adapter -> Adaptee.specific_request()
```

## Participants

- **Target**: Interface expected by the client.
- **Adapter**: Translates Target calls to the adaptee interface.
- **Adaptee**: Existing component with an incompatible interface.
- **Client**: Works against the Target abstraction.

## Forces

- Existing interfaces cannot be changed easily.
- Integration logic should be isolated.
- Multiple clients need a uniform API.

## Consequences

- **Benefit**: Enables reuse of existing components without polluting client code.
- **Cost**: Adds a translation layer that can hide impedance mismatches or performance costs.

## Smells

- Fixed: Scattered vendor-specific translation code, Clients tightly coupled to legacy APIs
- Created: Leaky adapters that expose adaptee quirks, Extra mapping overhead in hot paths

## Python sketch

```python
class LegacyPayments:
    def make_payment(self, cents: int) -> str:
        return f"paid:{cents}"

class PaymentPort:
    def charge(self, amount: float) -> str:
        raise NotImplementedError

class LegacyPaymentsAdapter(PaymentPort):
    def __init__(self, legacy: LegacyPayments):
        self.legacy = legacy

    def charge(self, amount: float) -> str:
        return self.legacy.make_payment(int(amount * 100))

svc = LegacyPaymentsAdapter(LegacyPayments())
print(svc.charge(12.34))
```

## Interview example

A CRUD API (04-crud-api) can adapt a legacy billing SDK to the application port so controllers depend on a stable interface, easing later migration.

## Related architecture patterns

- `04-crud-api`
- `layered`
- `microservices`

## Catalog subjects

- `technology/protocol`
