# patterns/papers

Interactive learning from research papers. Extract concepts, equations, and claims from arXiv papers, store as learnable entities, and visualize with interactive HTML.

## Quick Commands

```bash
just papers-ingest <arxiv-id>           # Download paper from arXiv, extract, store
just papers-render <arxiv-id>           # Generate HTML visualization
just papers-list                        # List all papers in knowledge base
```

## Workflow

1. **Ingest**: Download arXiv paper → extract concepts/equations/entities → store YAML
2. **Render**: Convert YAML → interactive HTML (concept map, equations, Q&A)
3. **Serve**: Access at `papers/<arxiv-id>/index.html`

## Paper Format

Each paper is stored as `content/arxiv-<id>.yaml`:
```yaml
arxiv_id: 2401.12345
title: "Paper Title"
authors: [Author1, Author2]
abstract: "..."
version: 1  # arXiv version (optional; defaults to latest)
date: 2026-11-10

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

## Outputs Generated

For each paper, `papers/<arxiv-id>/`:
- `README.md` — Paper summary, key contributions, learning path
- `index.html` — Interactive visualization (concept map, equations, Q&A)
- `concepts.json` — Concept graph (D3.js data)
- `equations.md` — LaTeX formulas extracted
- `glossary.json` — For spaced-repetition learning (patterns unified format)

## Integration

- **tool-lit-review**: Paper discovery and download
- **tool-rag**: Semantic search over paper content
- **math-trace**: Equation extraction and reproducibility
- **patterns/data-structures**: Cross-reference learning paths

## For universal rules, see `~/.claude/CLAUDE.md`.
