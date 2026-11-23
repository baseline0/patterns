# Patterns: Data Structures, Cloud Architecture, Game Theory

<!-- repo-role: content-and-rendering -->

**Reusable patterns for building and reasoning about systems.** Formerly `cloud-patterns`.

## Role and boundary

This repo is the **content and rendering layer**: teachable patterns, diagrams, scenarios, quizzes, and deterministic
builders that turn committed YAML and source docs into committed Markdown, HTML, glossaries, flashcards, and review
pages.

It does not acquire literature or index it:

- `tool-lit-review` searches, downloads, and analyses papers, then writes a schema-v1 `content-export`.
- `papers/tools/ingest.py` only **imports** that local export into `content/`. It never downloads, parses a PDF, or
  calls a sibling repo at runtime.
- `tool-rag` owns embedding and retrieval over PDFs. This repo consumes retrieval results; it does not store vectors.

The boundary in one line: **acquisition and analysis in `tool-lit-review`; content and presentation here; indexing and
retrieval in `tool-rag`.** A content build must run from committed files and local exports, with no network access.

### Design-intent guards

The boundary is enforced by tests, not prose. These run in `just test-unit` (the CI and pre-push gate):

| Invariant | Guard in `tests/unit/test_papers_content.py` |
|---|---|
| This repo declares the content role and names both neighbours | `test_readme_declares_the_content_role_and_neighbours` |
| No Python here imports a sibling tool or an acquisition/indexing library | `test_papers_tools_import_no_acquisition_or_indexing_code`, `test_no_python_in_the_repo_imports_a_sibling_tool` |
| PDFs stay in the producer's working folder, never in this repo | `test_papers_hold_no_pdf_files` |
| The importer refuses an unknown schema, an escaping PDF path, or a malformed checksum; a dry run writes nothing | `test_unknown_schema_is_refused`, `test_pdf_path_outside_the_folder_is_refused`, `test_dry_run_writes_nothing` |
| Re-import refreshes `source` metadata but preserves authored concepts, equations, claims and citations | `test_reimport_preserves_authored_fields` |
| Rendered output is derived only from committed YAML | `test_render_outputs_are_derived_from_committed_yaml` |
| Imported papers record original-summary rights, with no quoted PDF text | `test_imported_papers_record_original_summary_rights` |

Review surfaces follow the same rule: `tests/unit/test_cards.py`, `tests/unit/test_visual.py`, and
`tests/unit/test_proofs.py` regenerate checked-in outputs from committed sources and refuse acquisition or sibling imports.

## Start here (generated indexes)

Inventories are generated from source content. Use these instead of hand-maintained lists:

- **Primary local explorer:** `just -f site/justfile serve` → [site/index.html](site/index.html) (search/filter across families)
  Data: [site/catalog.json](site/catalog.json) · Pattern doc index: [patterns/PATTERNS_INDEX.md](patterns/PATTERNS_INDEX.md)
- **Architecture:** [architecture/CATALOGUE.md](architecture/CATALOGUE.md), [architecture/catalogue.json](architecture/catalogue.json), [architecture/graph.json](architecture/graph.json), [visual/architecture/index.html](visual/architecture/index.html)
- **Design patterns:** [design-patterns/INDEX.md](design-patterns/INDEX.md), [design-patterns/glossary.json](design-patterns/glossary.json)
- **Scenarios (canonical ladder):** [architecture/content/catalogue.yaml](architecture/content/catalogue.yaml) via [SCENARIOS.md](SCENARIOS.md), [scenarios/README.md](scenarios/README.md)
- **Providers:** [providers/matrix.md](providers/matrix.md), [providers/index.html](providers/index.html)
- **Cards:** [cards/index.html](cards/index.html), [cards/deck.json](cards/deck.json), [cards/anki.csv](cards/anki.csv)
- **Visual:** [visual/index.html](visual/index.html) (concept maps, diagrams, proof DAGs)
- **Proofs:** [proofs/README.md](proofs/README.md) (committed DAGs and generated notes/cards)
- **Papers:** [papers/README.md](papers/README.md) (imported metadata and rendered original summaries)
- **Data structures / Testing:** [data-structures/README.md](data-structures/README.md), [testing/README.md](testing/README.md)
- **Data engineering:** [data-engineering/README.md](data-engineering/README.md)

## Pattern families

- **Data structures:** how information is shaped, indexed, and kept consistent (see [data-structures/README.md](data-structures/README.md)).
- **Cloud architecture:** vendor-agnostic design patterns, taught through local emulators, IaC, and scenarios (current primary content; see site/catalogue).
- **Game theory:** subject data (strategic interaction, incentives, equilibria) lives in `catalog/game-theory/`; no teachable family here yet — see [ADR 0005](docs/adr/0005-catalog-boundary.md).

## Build and check

```bash
just -f site/justfile build && just -f site/justfile check
just -f proofs/justfile build && just -f visual/justfile build && just -f cards/justfile build
just validate
```

Study/review:
```bash
just -f site/justfile serve     # http://localhost:8000/site/index.html (primary)
just -f visual/justfile serve   # http://localhost:8000/visual/index.html
just -f cards/justfile review --minutes 30
```

### Relationship to `catalog`

<!-- catalog-boundary: subject-data-vs-pattern-rendering -->

`catalog` (L3, private) is the incubator for **domain subject data and provenance**: one folder per subject, with its
own sources and licence terms. This repo (L2, public) owns **reusable pattern structure, teaching content and
rendering**. Neither absorbs the other.

- This repo never imports, reads or ingests `catalog` at runtime or build time; a build runs from committed files only.
- Links to subjects are **references by ID** (`catalog_refs`: `subject` or `subject/id`), not copies of subject data and
  not absolute or parent-traversing paths. Source data and its terms stay in `catalog`.
- Overlap is split by ownership: `catalog` owns subject taxonomies (including `algorithms` and `game-theory`); this
  repo owns the teachable pattern layer (data structures, scenarios, quizzes, proof DAGs) and cites the subject by ID.
- When a subject matures it graduates to its own site repository, as `periodic-table-inspector` did. The builders here
  are a **template to copy**, not a dependency to import.

Decision record: [docs/adr/0005-catalog-boundary.md](docs/adr/0005-catalog-boundary.md). Contract tests:
[unit shape guards](tests/unit/test_catalog_contract.py) run in `just test`;
[host resolution](tests/host/test_catalog_refs.py) runs with `uv run pytest tests/host` when the catalog checkout is
beside this one (fleet workspace layout). The subject list is `catalog/subjects.json`, checked there by
`tests/test_subject_index.py`.

### How to add a catalog_ref

1. Pick a subject from `catalog/subjects.json`. Use `subject` for a whole subject, or `subject/id` for an entity in that
   subject's `ontology.yaml` (entity names are case- and punctuation-insensitive).
2. Add a `catalog_refs` list to the relevant content YAML. Keep it shallow: no paths, URLs, file names, imports or
   copied subject data.
3. Rebuild the affected family (`just -f architecture/justfile build` or `just -f design-patterns/justfile build`).
   Refs are rendered as non-linked provenance metadata.
4. Run `just test` and `uv run pytest tests/host -q`. A bad ref fails with `unknown subject`, `subject has no ontology`,
   `unknown entity`, or `unresolved catalog_refs`.

## Philosophy

- **Vendor-agnostic:** patterns first, provider details second
- **Cost-free:** local emulators and `terraform plan` / validation workflows
- **IaC-first:** infrastructure described as code where applicable
- **Scenario-driven:** learn through architecture exercises
- **Diagram + code:** visuals paired with implementations and generated views

## References and contributing

- External references: [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/), [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/), [GCP Architecture Framework](https://cloud.google.com/architecture/framework), [Terraform](https://www.terraform.io/docs/), [Draw.io](https://draw.io)
- Learning path: [LEARNING.md](LEARNING.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- License: MIT (see [LICENSE](LICENSE))
