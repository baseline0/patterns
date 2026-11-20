# Builder

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: creational

**Intent**: Separate construction of a complex object from its representation so the same process can create different forms.

## Problem

Creating objects with many optional parts, validation rules, or assembly steps leads to telescoping constructors and fragile setup code.

## Structure

```text
Director -> Builder.build_part()
Builder -> assembles Product
ConcreteBuilder returns specific Product representation
```

## Participants

- **Builder**: Declares steps for constructing parts of the product.
- **ConcreteBuilder**: Implements steps and keeps the product being assembled.
- **Director**: Orchestrates construction steps in a particular order.
- **Product**: The complex object produced by the builder.

## Forces

- Construction requires multiple ordered steps or validation.
- Different representations share a construction process.
- Clients should not manage partial, invalid states.

## Consequences

- **Benefit**: Improves readability and correctness for complex object assembly.
- **Cost**: Adds classes/objects and can be overkill for simple data structures.

## Smells

- Fixed: Telescoping constructors with many optional parameters, Ad hoc assembly code repeated across call sites
- Created: Boilerplate builder classes, Stale directors when construction steps diverge

## Python sketch

```python
class RequestBuilder:
    def __init__(self):
        self._headers = {}
        self._timeout = 30

    def header(self, k: str, v: str):
        self._headers[k] = v
        return self

    def timeout(self, seconds: int):
        self._timeout = seconds
        return self

    def build(self) -> dict:
        if self._timeout <= 0:
            raise ValueError("timeout")
        return {"headers": dict(self._headers), "timeout": self._timeout}

req = RequestBuilder().header("x-trace", "1").timeout(10).build()
print(req)
```

## Interview example

A CI/CD deployment definition (06-cicd-pipeline) can use a builder to assemble validated pipeline specs (stages, retries, artifacts) before submitting to the platform.

## Related architecture patterns

- `06-cicd-pipeline`
- `layered`
- `cqrs`
