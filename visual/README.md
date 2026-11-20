# Visual review

Static, deterministic pages that turn committed content into something you can look at and recall. Everything here is
generated from this repository; there are no network requests, CDN scripts, or sibling-repo imports.

| Page | Source | Purpose |
| --- | --- | --- |
| `index.html` | all inventories | hub for the four review modes |
| `concepts/arxiv-*.html` | `papers/content/*.yaml` | concept map + equations + claims to defend |
| `diagrams/index.html` | `data/patterns.json`, `assets/diagrams/*.svg` | original architecture diagrams with decision captions |
| `proofs/index.html` | `proofs/content/*.yaml` | three real proof DAGs for interview drills |

## Commands

```bash
just -f visual/justfile build
just -f visual/justfile check
just -f visual/justfile serve   # http://localhost:8000/visual/index.html
```

## Concept maps

Add `related: [other-concept-id]` to a concept in a paper YAML to draw an edge. Nodes without `related` still render;
the graph is a static SVG laid out on a circle, so output is byte-stable and reviewable in a diff.

## Adding proof graphs

Add another `proofs/content/<id>.yaml` beside the three committed DAGs:

```yaml
id: induction-on-loop
title: Induction on a loop invariant
statement: "After k iterations, prefix[0:k] is sorted."
invariant: "The processed prefix is always sorted."
steps:
  - id: base
    label: "Base case k=0"
    detail: "The empty prefix is sorted."
  - id: step
    label: "Inductive step"
    detail: "Insert the next element into its sorted position."
    depends_on: [base]
complexity: "O(n^2) insertions; O(n log n) with binary insertion."
```

`depends_on` gives the DAG edges; cycles and unknown ids fail the build. `tests/unit/test_visual.py` checks the renderer
and `tests/unit/test_proofs.py` checks the YAML, claim links, and generated cards.
