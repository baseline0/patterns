# Prototype

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: creational

**Intent**: Create new objects by copying a prototypical instance instead of instantiating from scratch.

## Problem

Object creation is expensive or configuration-heavy, and new instances should start from known templates with small variations.

## Structure

```text
Client -> Prototype.clone()
ConcretePrototype implements clone() -> returns copy
Registry may store named prototypes
```

## Participants

- **Prototype**: Declares a cloning operation.
- **ConcretePrototype**: Implements cloning, including deep-copy decisions.
- **Client**: Requests new objects by cloning prototypes.
- **PrototypeRegistry**: Optionally stores and retrieves canonical prototypes by key.

## Forces

- Initialization cost or complexity is high.
- Instances share a baseline configuration.
- Copies must define clear deep vs shallow semantics.

## Consequences

- **Benefit**: Speeds creation and centralizes default templates.
- **Cost**: Cloning graphs with shared references or cycles can be error-prone.

## Smells

- Fixed: Repeated expensive setup code for similar objects, Large configuration blocks duplicated across constructors
- Created: Accidental sharing of mutable nested state, Hidden copy semantics

## Python sketch

```python
import copy
from dataclasses import dataclass, field

@dataclass
class JobTemplate:
    image: str
    env: dict = field(default_factory=dict)

    def clone(self, **overrides):
        new = copy.deepcopy(self)
        for k, v in overrides.items():
            setattr(new, k, v)
        return new

base = JobTemplate("python:3.12", {"REGION": "us-east-1"})
canary = base.clone(env={"REGION": "us-east-1", "CANARY": "1"})
print(base.env, canary.env)
```

## Interview example

In a CI/CD system (06-cicd-pipeline), pipeline job templates can be cloned per environment so baseline steps stay consistent while overrides remain explicit.

## Related architecture patterns

- `06-cicd-pipeline`
- `serverless`
- `layered`
