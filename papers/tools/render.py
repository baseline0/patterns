#!/usr/bin/env python3
"""Render committed paper YAML into local learning outputs.

Input: content/arxiv-<id>.yaml, written by import-export and then authored here.
Output:
- README.md (paper summary)
- index.html (interactive visualization)
- concepts.json (concept graph)
- equations.md (LaTeX formulas)
- glossary.json (for spaced repetition)

This renderer does no acquisition: no network, no PDF parsing, no sibling-repo import. Paper download and metadata
export belong to tool-lit-review; indexing and retrieval belong to tool-rag.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import typer
import yaml

app = typer.Typer(help="Render committed paper YAML into local learning outputs.")
ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


def _text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _items(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def glossary(paper: dict[str, Any], topic: str) -> list[dict[str, Any]]:
    """Flashcards for the patterns unified glossary format: one per concept and one per claim."""
    entries: list[dict[str, Any]] = []
    for concept in _items(paper.get("concepts")):
        name = _text(concept.get("name")) or _text(concept.get("id")) or "concept"
        entries.append(
            {
                "title": f"Concept: {name}",
                "body": _text(concept.get("definition")),
                "metadata": {"tags": [topic, "concept"]},
            }
        )
    for claim in _items(paper.get("claims")):
        entries.append(
            {
                "title": f"Claim: {_text(claim.get('section')) or topic}",
                "body": _text(claim.get("text")),
                "metadata": {"tags": [topic, "claim"], "support_level": _text(claim.get("support_level"))},
            }
        )
    return entries


def concept_graph(paper: dict[str, Any]) -> dict[str, Any]:
    """D3-friendly nodes for each concept. Links stay empty until citations carry concept ids."""
    nodes = [
        {
            "id": _text(concept.get("id")) or f"concept-{index}",
            "label": _text(concept.get("name")) or _text(concept.get("id")),
            "definition": _text(concept.get("definition")),
            "mentions": concept.get("mentions", 0),
        }
        for index, concept in enumerate(_items(paper.get("concepts")), start=1)
    ]
    return {"nodes": nodes, "links": []}


def _readme(paper: dict[str, Any], topic: str) -> str:
    title = _text(paper.get("title")) or topic
    lines = [f"# {title}", "", "> Generated from `content/`. Edit the YAML, then run `tools/render.py`.", "", f"- Open in explorer: `../../site/index.html#papers:paper:{topic}` (`just -f site/justfile serve`)", ""]
    authors = paper.get("authors")
    if isinstance(authors, list) and authors:
        lines += [f"**Authors**: {', '.join(str(author) for author in authors)}", ""]
    abstract = _text(paper.get("abstract"))
    if abstract:
        lines += ["## Abstract", "", abstract, ""]
    concepts = _items(paper.get("concepts"))
    if concepts:
        lines += ["## Concepts", ""]
        lines += [f"- **{_text(c.get('name')) or _text(c.get('id'))}**: {_text(c.get('definition'))}" for c in concepts]
        lines.append("")
    equations = _items(paper.get("equations"))
    if equations:
        lines += ["## Equations", ""]
        for equation in equations:
            lines.append(f"- `{_text(equation.get('latex'))}` — {_text(equation.get('description'))}")
        lines.append("")
    claims = _items(paper.get("claims"))
    if claims:
        lines += ["## Claims", ""]
        for claim in claims:
            section = _text(claim.get("section"))
            support = _text(claim.get("support_level"))
            suffix = f" ({section}; {support})" if section or support else ""
            lines.append(f"- {_text(claim.get('text'))}{suffix}")
        lines.append("")
    source = paper.get("source")
    if isinstance(source, dict) and source.get("paper_id"):
        lines += ["## Source", "", f"- Paper: `{source.get('paper_id')}`", f"- PDF: `{source.get('pdf')}`"]
        if source.get("licence"):
            lines.append(f"- Licence: {source['licence']}")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def _equations_md(paper: dict[str, Any], topic: str) -> str:
    lines = [f"# Equations: {_text(paper.get('title')) or topic}", ""]
    equations = _items(paper.get("equations"))
    if not equations:
        lines.append("No equations recorded.")
    for equation in equations:
        lines += [
            f"## {_text(equation.get('id')) or 'equation'}",
            "",
            f"```latex\n{_text(equation.get('latex'))}\n```",
            "",
            _text(equation.get("description")),
            "",
            f"Section: {_text(equation.get('section')) or 'n/a'}",
            "",
        ]
    return "\n".join(lines).rstrip("\n") + "\n"


def _index_html(paper: dict[str, Any], topic: str) -> str:
    esc = html.escape
    title = _text(paper.get("title")) or topic
    parts = [
        "<!doctype html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(title)}</title>",
        "<style>body{font-family:system-ui,sans-serif;max-width:52rem;margin:2rem auto;padding:0 1rem;line-height:1.5}"
        "code{background:#f3f3f3;padding:0 .2rem}nav a{margin-right:1rem}</style>",
        "</head><body>",
        f'<nav><a href="../../site/index.html#papers:paper:{topic}">Explorer</a><a href="../../visual/index.html">Visual hub</a><a href="../../cards/index.html">Cards</a></nav>',
        f"<h1>{esc(title)}</h1>",
    ]
    if _text(paper.get("abstract")):
        parts.append(f"<h2>Abstract</h2><p>{esc(_text(paper.get('abstract')))}</p>")
    for concept in _items(paper.get("concepts")):
        name = _text(concept.get("name")) or _text(concept.get("id"))
        parts.append(f"<h2>{esc(name)}</h2><p>{esc(_text(concept.get('definition')))}</p>")
    for equation in _items(paper.get("equations")):
        parts.append(f"<h2>Equation {esc(_text(equation.get('id')))}</h2>")
        parts.append(f"<pre><code>{esc(_text(equation.get('latex')))}</code></pre>")
        parts.append(f"<p>{esc(_text(equation.get('description')))}</p>")
    parts.append("</body></html>")
    return "\n".join(parts) + "\n"


def render_outputs(paper: dict[str, Any], topic: str) -> dict[str, str]:
    """Every output as text, keyed by file name. Pure, so tests can compare without writing."""
    return {
        "README.md": _readme(paper, topic),
        "index.html": _index_html(paper, topic),
        "concepts.json": json.dumps(concept_graph(paper), indent=2, ensure_ascii=False) + "\n",
        "equations.md": _equations_md(paper, topic),
        "glossary.json": json.dumps(glossary(paper, topic), indent=2, ensure_ascii=False) + "\n",
    }


@app.command()
def render(arxiv_id: str = typer.Argument(..., help="arXiv ID (e.g., 2401.12345)")) -> None:
    """Render one committed paper YAML into its output folder. No network, no PDF parsing."""
    arxiv_id_clean = arxiv_id.replace("/", ".") if "/" in arxiv_id else arxiv_id
    yaml_file = CONTENT / f"arxiv-{arxiv_id_clean}.yaml"

    if not yaml_file.exists():
        typer.echo(f"Paper not found: {yaml_file}", err=True)
        raise typer.Exit(1)

    with open(yaml_file, encoding="utf-8") as handle:
        paper = yaml.safe_load(handle)
    if not isinstance(paper, dict):
        typer.echo(f"{yaml_file} must hold a YAML mapping", err=True)
        raise typer.Exit(1)

    output_dir = ROOT / arxiv_id_clean
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = render_outputs(paper, arxiv_id_clean)
    for name, text in outputs.items():
        (output_dir / name).write_text(text, encoding="utf-8")
    typer.echo(f"Rendered {len(outputs)} file(s): {output_dir}/")
    for name in outputs:
        typer.echo(f"  - {name}")


if __name__ == "__main__":
    app()
