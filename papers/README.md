# Papers: Imported Content and Local Rendering

Turn papers acquired by `tool-lit-review` into committed learning content.

This folder is part of `patterns`, the content and rendering layer. It never downloads, fetches, parses, or indexes a
paper. Acquisition and analysis belong to `tool-lit-review`; vector indexing and retrieval belong to `tool-rag`.

**Workflow**:

1. In `tool-lit-review`: search, select, and fetch the paper (licence gate, pacing, checksum manifest).
2. In `tool-lit-review`: write the content export.
   ```bash
   uv run tool-lit-review content-export --papers <working-folder> --output /tmp/papers.json
   ```
3. Here: import the local export into committed YAML.
   ```bash
   just -f papers/justfile import-export /tmp/papers.json
   ```
4. Author the concepts, equations, and claims in `content/arxiv-<id>.yaml`; render with the render recipe.

**Example**:
```bash
just -f papers/justfile import-export /tmp/papers.json
just -f papers/justfile render 2401.12345
# Opens: papers/2401.12345/index.html
```

**Why the split**: one repo owns the downloader, licence gate, pacing, and checksum manifest, so there is one place to
audit them. This repo keeps only committed content and deterministic local tooling, so a content build needs no
network and no sibling checkout at runtime.

**Import rules**: re-importing preserves authored concepts, equations, claims, and citations. The importer refuses an
unknown export schema, a path outside the papers folder, or a malformed checksum.

See [CLAUDE.md](CLAUDE.md) for the format and commands.
