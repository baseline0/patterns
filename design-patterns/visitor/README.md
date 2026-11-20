# Visitor

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Category**: behavioral

**Intent**: Represent an operation to be performed on elements of an object structure without changing the element classes.

## Problem

Adding new operations across a stable set of element types leads to repeated edits and scattered logic in those classes.

## Structure

```text
Element.accept(visitor)
Visitor.visitElementA/B(...)
ConcreteVisitor implements operations across elements
```

## Participants

- **Visitor**: Declares visit operations for each concrete element type.
- **ConcreteVisitor**: Implements a specific operation over the structure.
- **Element**: Declares accept to dispatch to the visitor.
- **ConcreteElement**: Implements accept by calling the matching visit method.

## Forces

- Element hierarchy is stable but operations change often.
- Related behavior should be grouped by operation.
- Double dispatch or equivalent is available.

## Consequences

- **Benefit**: Makes adding new operations easy and keeps operation-specific logic cohesive.
- **Cost**: Adding new element types requires changing every visitor.

## Smells

- Fixed: Operation logic scattered across many element classes, Repeated type switches to perform operations over a structure
- Created: Visitor interface churn when elements change, Tight coupling between visitors and element set

## Python sketch

```python
class Number:
    def __init__(self, value):
        self.value = value

    def accept(self, v):
        return v.visit_number(self)

class SumVisitor:
    def __init__(self):
        self.total = 0

    def visit_number(self, n):
        self.total += n.value

nums = [Number(1), Number(2), Number(3)]
vis = SumVisitor()
for n in nums:
    n.accept(vis)
print(vis.total)
```

## Interview example

In a CI/CD or policy engine (06-cicd-pipeline), visitors can run lint, cost, or security analyses over a stable pipeline AST without modifying node classes.

## Related architecture patterns

- `06-cicd-pipeline`
- `pipe-and-filter`
- `layered`
