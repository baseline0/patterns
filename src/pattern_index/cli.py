"""CLI for the patterns index."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from .index import get_pattern, list_families, list_patterns, search_patterns

app = typer.Typer(help="Patterns index (read-only).", add_completion=False)


@app.command("families")
def families_command(root: Path | None = typer.Option(None, "--root")) -> None:
    for family in list_families(root):
        typer.echo(family)


@app.command("list")
def list_command(family: str | None = typer.Option(None, "--family"), root: Path | None = typer.Option(None, "--root")) -> None:
    for item in list_patterns(family=family, root=root):
        typer.echo(f"{item.id}\t{item.family}\t{item.title}")


@app.command("search")
def search_command(query: str, root: Path | None = typer.Option(None, "--root")) -> None:
    for item in search_patterns(query, root=root):
        typer.echo(f"{item.id}\t{item.title}")


@app.command("show")
def show_command(pattern_id: str, root: Path | None = typer.Option(None, "--root")) -> None:
    item = get_pattern(pattern_id, root=root)
    if item is None:
        typer.echo(f"not found: {pattern_id}", err=True)
        raise typer.Exit(code=1)
    typer.echo(json.dumps({"id": item.id, "title": item.title, "family": item.family, "kind": item.kind,
                           "summary": item.summary, "source": item.source, "tags": item.tags}, indent=2))


if __name__ == "__main__":
    app()
