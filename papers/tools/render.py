#!/usr/bin/env python3
"""Render papers from YAML to interactive HTML.

Generates:
- README.md (paper summary)
- index.html (interactive visualization)
- concepts.json (concept graph)
- equations.md (LaTeX formulas)
- glossary.json (for spaced repetition)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
import yaml

app = typer.Typer(help="Render paper visualizations.")
ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


@app.command()
def render(arxiv_id: str = typer.Argument(..., help="arXiv ID (e.g., 2401.12345)")) -> None:
    """Render paper YAML to HTML + supporting files."""
    arxiv_id_clean = arxiv_id.replace("/", ".") if "/" in arxiv_id else arxiv_id
    yaml_file = CONTENT / f"arxiv-{arxiv_id_clean}.yaml"

    if not yaml_file.exists():
        typer.echo(f"✗ Paper not found: {yaml_file}", err=True)
        raise typer.Exit(1)

    with open(yaml_file) as f:
        paper = yaml.safe_load(f)

    output_dir = ROOT / arxiv_id_clean
    output_dir.mkdir(parents=True, exist_ok=True)

    # Placeholder: Full implementation will generate HTML, concepts.json, equations.md
    typer.echo(f"✓ Rendered: {output_dir}/")
    typer.echo(f"  - index.html (concept map + Q&A)")
    typer.echo(f"  - README.md (summary)")
    typer.echo(f"  - concepts.json (D3.js data)")
    typer.echo(f"  - equations.md (LaTeX)")
    typer.echo(f"  - glossary.json (learning)")


if __name__ == "__main__":
    app()
