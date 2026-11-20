# Scenario drills

`tools/drill.py` turns the committed scenario ladder into timed system-design practice. The canonical scenario list lives
in `architecture/content/catalogue.yaml`; each entry must have a prompt, hints, model solution, and rubric.

```bash
just -f scenarios/justfile list
just -f scenarios/justfile drill 09-microservices --minutes 45 --dry-run
just -f scenarios/justfile reveal 10-disaster-recovery --section rubric
```

Your notes are stored only in `scenarios/.drill-state.json`, which is gitignored. `--dry-run` previews without writing.
