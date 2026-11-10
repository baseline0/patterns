# Papers: Interactive Learning from Research

Transform arXiv papers into interactive learning experiences.

**Workflow**:
1. Specify arXiv ID
2. Download paper → extract concepts, equations, entities
3. Generate interactive HTML (concept map, Q&A, equation browser)
4. Learn through exploration and retrieval

**Example**:
```bash
just papers-ingest arxiv:2401.12345
just papers-render arxiv:2401.12345
# Opens: papers/2401-12345/index.html
```

See [CLAUDE.md](CLAUDE.md) for details.
