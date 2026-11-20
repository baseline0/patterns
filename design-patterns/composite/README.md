# Composite

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: structural

**Intent**: Compose objects into tree structures and let clients treat individual objects and compositions uniformly.

## Problem

Client code must distinguish leaves from containers when operating over hierarchical structures, leading to special-case logic.

## Structure

```text
Component.operation()
Leaf implements Component
Composite holds children: [Component]
Composite.operation() delegates to children
```

## Participants

- **Component**: Common interface for leaves and composites.
- **Leaf**: Represents end objects with no children.
- **Composite**: Stores children and implements operations by delegating to them.
- **Client**: Manipulates the tree through the Component interface.

## Forces

- Part-whole hierarchies must be represented.
- Clients should ignore leaf vs container differences.
- Operations should apply recursively over the structure.

## Consequences

- **Benefit**: Simplifies client code and makes it easy to add new component types.
- **Cost**: Can make it harder to restrict which children a composite may contain.

## Smells

- Fixed: Type checks and branching for leaf vs group handling, Duplicated tree traversal logic in clients
- Created: Overly general component interfaces, Difficulty enforcing structural constraints

## Python sketch

```python
class Node:
    def size(self) -> int:
        raise NotImplementedError

class File(Node):
    def __init__(self, bytes_: int):
        self.bytes_ = bytes_

    def size(self) -> int:
        return self.bytes_

class Folder(Node):
    def __init__(self, children):
        self.children = children

    def size(self) -> int:
        return sum(c.size() for c in self.children)

tree = Folder([File(10), Folder([File(5), File(3)])])
print(tree.size())
```

## Interview example

A static website asset pipeline (01-static-website) can treat files and directories uniformly when computing deploy manifests or cache invalidation sets.

## Related architecture patterns

- `01-static-website`
- `pipe-and-filter`
- `layered`
