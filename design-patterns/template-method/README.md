# Template Method

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: behavioral

**Intent**: Define the skeleton of an algorithm in a base operation, deferring specific steps to subclasses or hooks.

## Problem

Multiple implementations share the same overall process but duplicate its structure while varying a few steps.

## Structure

```text
AbstractClass.template() calls step1(), step2(), hook()
ConcreteClass overrides variable steps
Invariant sequence stays in base class
```

## Participants

- **AbstractClass**: Defines the template method and invariant algorithm structure.
- **ConcreteClass**: Implements or overrides variable steps of the algorithm.

## Forces

- Algorithm structure is stable but some steps vary.
- Code duplication appears across similar workflows.
- Control over step order must remain centralized.

## Consequences

- **Benefit**: Reuses invariant workflow logic and enforces consistent sequencing.
- **Cost**: Relies on inheritance and can make flows harder to follow across class hierarchy.

## Smells

- Fixed: Copied-pasted workflow methods with minor variations, Inconsistent step ordering across implementations
- Created: Fragile base class hierarchies, Subclasses constrained by inheritance-based extension

## Python sketch

```python
class ImportJob:
    def run(self, source: str) -> dict:
        data = self.extract(source)
        rows = self.transform(data)
        return self.load(rows)

    def extract(self, source: str):
        raise NotImplementedError

    def transform(self, data):
        return [x.strip() for x in data]

    def load(self, rows):
        return {"count": len(rows)}

class CsvImport(ImportJob):
    def extract(self, source: str):
        return source.split(",")

print(CsvImport().run("a, b, c"))
```

## Interview example

A pipe-and-filter data pipeline (pipe-and-filter) can define a fixed ingest-transform-load skeleton while subclasses customize extraction per source.

## Related architecture patterns

- `pipe-and-filter`
- `08-streaming`
- `layered`
