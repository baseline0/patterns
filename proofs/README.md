# Proofs

- **Explore in local catalogue:** run `just -f site/justfile serve` and open `site/index.html` (searchable, cross-linked).
- **Lean 4 tactics:** [lean4-tactics.md](lean4-tactics.md) — common tactics and when to use them.

Interview-grade proof skeletons stored as small dependency DAGs. Each file in `content/` is the source of truth;
`tools/build.py` renders notes and glossary cards, and `visual/tools/build.py` renders the DAG page.

## Schema

```yaml
id: stable-kebab-id
title: Human-readable name
family: data-structures
claim_ids: [claim-this-proof-justifies]
statement: "What is being proved."
invariant: "The condition preserved at each step."
steps:
  - id: base
    label: "Base case"
    detail: "Why it starts true."
  - id: step
    label: "Inductive step"
    detail: "Why it stays true."
    depends_on: [base]
complexity: "Bound and space use."
```

`depends_on` names earlier step ids; unknown ids, self-dependencies, and duplicate step ids fail the build. The current
proofs justify the dynamic-array, sliding-window, and heapify claims in `data-structures/`.

## Commands

```bash
just -f proofs/justfile build
just -f proofs/justfile check
just -f visual/justfile build
just -f cards/justfile build
```

Proof steps become cards tagged with the proof id, so they join the timed review deck automatically.
