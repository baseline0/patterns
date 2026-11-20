# Memento

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

**Category**: behavioral

**Intent**: Capture and externalize an object’s internal state so it can be restored later without violating encapsulation.

## Problem

Implementing undo, checkpoints, or rollback requires access to internal state that should remain private.

## Structure

```text
Originator.create_memento() -> Memento(state)
Caretaker stores Memento
Originator.restore(memento) -> reinstates state
```

## Participants

- **Originator**: Creates mementos from its state and restores from them.
- **Memento**: Stores a snapshot of the originator’s internal state.
- **Caretaker**: Keeps mementos without inspecting or modifying their contents.

## Forces

- Undo/rollback capability is required.
- Internal state must stay encapsulated.
- Snapshots may be frequent or large.

## Consequences

- **Benefit**: Supports rollback and checkpoints while preserving encapsulation boundaries.
- **Cost**: Can consume significant memory or require careful snapshot sizing.

## Smells

- Fixed: Exposing private fields just to support undo, Ad hoc rollback logic scattered across callers
- Created: High memory usage from frequent snapshots, Caretakers retaining mementos longer than needed

## Python sketch

```python
class Editor:
    def __init__(self):
        self.text = ""

    def write(self, s: str):
        self.text += s

    def save(self) -> tuple:
        return (self.text,)

    def restore(self, snap: tuple):
        self.text = snap[0]

ed = Editor(); ed.write("a"); snap = ed.save(); ed.write("b"); ed.restore(snap)
print(ed.text)
```

## Interview example

A CQRS command side (cqrs) can snapshot aggregate state before applying a risky command, enabling controlled rollback or debugging without leaking internals.

## Related architecture patterns

- `cqrs`
- `event-driven`
- `layered`
