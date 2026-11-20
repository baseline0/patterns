# System design scenario drills

The canonical scenario ladder and required artifacts are defined in `architecture/content/catalogue.yaml` and indexed in generated artifacts:

- [Architecture catalogue](architecture/CATALOGUE.md) — canonical scenario list, statuses, and links
- [Architecture graph](architecture/graph.json) / [visual graph](visual/architecture/index.html)
- [Site explorer](site/index.html) (`just -f site/justfile serve`) — searchable view of scenarios and all other content

Each scenario directory under `scenarios/<id>/` contains committed artifacts (for example `README.md`, `HINTS.md`, `SOLUTION.md`, `RUBRIC.md`) as recorded in the catalogue.

## Commands

```bash
just -f scenarios/justfile list
just -f scenarios/justfile drill 09-microservices --minutes 45 --dry-run
just -f scenarios/justfile reveal 10-disaster-recovery --section rubric
just -f architecture/justfile build   # regenerate catalogue/index artifacts
just -f site/justfile build           # regenerate site catalog and patterns index
```

Notes are stored only in `scenarios/.drill-state.json` (gitignored). `--dry-run` previews without writing.

> Edit scenario content in source files and `architecture/content/catalogue.yaml`, then rebuild generated outputs. Do not hand-maintain generated indexes.
