# patterns/papers

Imported paper content and local rendering. Import metadata from a `tool-lit-review` export, author concepts,
equations, and claims as learnable entities, and render with committed local tools.

This folder does **not** download, fetch, parse, or index papers. `tool-lit-review` owns acquisition and analysis;
`tool-rag` owns indexing and retrieval.

## Quick Commands

```bash
just -f papers/justfile import-export /tmp/papers.json   # Import a local tool-lit-review content export
just -f papers/justfile render <arxiv-id>                # Generate HTML visualization from committed YAML
just -f papers/justfile list                             # List all papers in the knowledge base
```

## Workflow

1. **Acquire elsewhere**: in `tool-lit-review`, search, select, fetch, then run `content-export`.
2. **Import**: read the schema-v1 export → update committed YAML, preserving authored fields.
3. **Render**: convert committed YAML → committed HTML (concept map, equations, Q&A).
4. **Serve**: access at `papers/<arxiv-id>/index.html`.

No step here calls the network or imports a sibling repo at runtime.

## Paper Format

Each paper is stored as `content/arxiv-<id>.yaml`. The importer owns the `source` block; authors own everything else:
```yaml
arxiv_id: 2401.12345
title: "Paper Title"
authors: [Author1, Author2]
abstract: "..."
version: 1  # arXiv version (optional; defaults to latest)
date: 2026-11-10

rights:  # authored; required when source has no licence
  quotes: none
  basis: original-summary
  note: "Metadata came from a tool-lit-review export; no PDF text or quoted abstract is stored here."

source:  # written by import-export; do not edit by hand
  tool: tool-lit-review
  schema_version: 1
  paper_id: 2401.12345
  sha256: "<64 hex characters>"
  pdf: pdf/2401.12345.pdf
  exported_at: 2026-11-10T14:29:02+00:00
  licence: https://creativecommons.org/licenses/by/4.0/

concepts:
  - id: concept-1
    name: "Concept Name"
    definition: "..."
    mentions: 3

equations:
  - id: eq-1
    latex: "E = mc^2"
    description: "Einstein's mass-energy equivalence"
    section: "Introduction"

entities:
  people: [{name: "Name", orcid: "..."}, ...]
  organizations: [{name: "Name", ror: "..."}, ...]

claims:
  - text: "Key claim from paper"
    section: "Methodology"
    support_level: "experimental"

citations:
  - arxiv_id: 2401.00001
    title: "Cited Paper"
    relation: "builds_on"
```

When `source` has no licence, write an original summary and keep `rights.quotes: none`; the unit gate rejects a missing
rights block on an imported paper. Short attributed quotes need a licence gate and a human rights check upstream.

## Outputs Generated

For each paper, `papers/<arxiv-id>/`:
- `README.md` — Paper summary, key contributions, learning path
- `index.html` — Interactive visualization (concept map, equations, Q&A)
- `concepts.json` — Concept graph (D3.js data)
- `equations.md` — LaTeX formulas extracted
- `glossary.json` — For spaced-repetition learning (patterns unified format)

## Integration

- **tool-lit-review**: Paper discovery, download, and the `content-export` contract consumed here
- **tool-rag**: Semantic search over paper content (indexing and retrieval live there)
- **math-trace**: Equation extraction and reproducibility
- **patterns/data-structures**: Cross-reference learning paths

## For universal rules, see `~/.claude/CLAUDE.md`.
