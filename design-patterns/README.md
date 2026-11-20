# Design patterns

Object and application patterns that bridge data-structure reasoning and system architecture. Each file in `content/` is
the source of truth; `tools/build.py` renders notes, quizzes, HTML, and a `glossary.json` that joins the canonical deck.
The generated pattern list lives in `INDEX.md`.

## Schema

```yaml
id: strategy
name: Strategy
category: behavioral
intent: "One sentence: what it does."
problem: "The design pressure that makes it useful."
structure: |
  Context --> Strategy
       |        ^
       +--> ConcreteStrategy
participants:
  - name: Context
    role: "Delegates the varying behaviour."
forces: ["Which force is balanced?"]
consequences:
  benefit: "What improves."
  cost: "What it makes harder."
smells_fixed: ["switch-on-type"]
smells_created: ["more classes"]
python: |
  class Context:
      def __init__(self, strategy): self.strategy = strategy
example: "Interview example."
related_architecture: [layered, event-driven]
quiz:
  - question: "When is Strategy preferable?"
    choices: ["When algorithms vary", "When state is global"]
    answer: 0
    explanation: "Strategy encapsulates interchangeable behaviour."
```

`related_architecture` must name an architecture style, tactic, or scenario in the canonical catalogue. Quiz answers are
zero-based.

## Commands

```bash
just -f design-patterns/justfile build
just -f design-patterns/justfile check
just -f design-patterns/justfile quiz --category behavioral
just -f design-patterns/justfile list
```
