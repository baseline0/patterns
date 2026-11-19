"""Render committed content into deterministic visual review pages.

Inputs are repository files only: papers/content YAML, data/patterns.json, assets/diagrams, and optional
proofs/content YAML. No network, no PDF parsing, no CDN assets, no sibling-repo imports. Every output is pure text so
tests can regenerate and compare it without writing.
"""

from __future__ import annotations

import html
import json
import math
from pathlib import Path
from typing import Any

import typer
import yaml

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent
PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
body{font-family:system-ui,sans-serif;max-width:60rem;margin:2rem auto;padding:0 1rem;line-height:1.5}
h1,h2{margin-top:1.8rem}nav a{margin-right:1rem}figure{margin:1.5rem 0;border:1px solid #8884;border-radius:8px;padding:1rem}
img{max-width:100%;height:auto}pre{background:#8882;padding:.8rem;overflow:auto;border-radius:6px}
.meta{color:#888;font-size:.85rem}table{border-collapse:collapse;width:100%}td,th{border:1px solid #8884;padding:.4rem;text-align:left}
svg{max-width:100%;height:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:1rem}
</style></head><body>
<nav><a href="__HUB__">Visual hub</a><a href="__CARDS__">Cards</a><a href="__SECTION__">Section index</a></nav>
__BODY__
</body></html>
"""


class ContentError(ValueError):
    """A committed visual source is malformed."""


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def items(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def page(title: str, body: str, section: bool = False) -> str:
    """Section pages are one directory deeper than the hub, so their card link goes one level further up."""
    links = {
        "__HUB__": "../index.html" if section else "index.html",
        "__CARDS__": "../../cards/index.html" if section else "../cards/index.html",
        "__SECTION__": "index.html",
    }
    rendered = PAGE.replace("__TITLE__", esc(title)).replace("__BODY__", body)
    for token, href in links.items():
        rendered = rendered.replace(token, href)
    return rendered


def load_papers(root: Path = REPO_ROOT) -> list[tuple[str, dict[str, Any]]]:
    papers = []
    for path in sorted((root / "papers" / "content").glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ContentError(f"{path.name}: expected a YAML mapping")
        topic = text(payload.get("arxiv_id")) or path.stem.removeprefix("arxiv-")
        papers.append((topic, payload))
    if not papers:
        raise ContentError("no committed papers/content YAML found")
    return papers


def load_patterns(root: Path = REPO_ROOT) -> list[dict[str, Any]]:
    payload = json.loads((root / "data" / "patterns.json").read_text(encoding="utf-8"))
    return items(payload.get("patterns"))


def load_proofs(root: Path = REPO_ROOT) -> list[tuple[str, dict[str, Any]]]:
    proofs = []
    for path in sorted((root / "proofs" / "content").glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ContentError(f"{path.name}: expected a YAML mapping")
        proofs.append((text(payload.get("id")) or path.stem, payload))
    return proofs


def concept_graph(paper: dict[str, Any]) -> dict[str, Any]:
    """Concept nodes with optional `related` links; links stay empty until authors add them."""
    concepts = items(paper.get("concepts"))
    nodes = []
    for index, concept in enumerate(concepts):
        node_id = text(concept.get("id")) or f"concept-{index + 1}"
        label = text(concept.get("name")) or node_id
        nodes.append(
            {
                "id": node_id,
                "label": label,
                "definition": text(concept.get("definition")),
                "mentions": concept.get("mentions", 0),
                "related": [text(value) for value in concept.get("related", []) if text(value)],
            }
        )
    known = {node["id"] for node in nodes}
    links = [
        {"source": node["id"], "target": target}
        for node in nodes
        for target in dict.fromkeys(node["related"])
        if target in known and target != node["id"]
    ]
    return {"nodes": nodes, "links": links}


def concept_svg(graph: dict[str, Any]) -> str:
    """Static SVG concept map: deterministic circle layout, no JavaScript or remote libraries."""
    nodes = graph["nodes"]
    if not nodes:
        return '<p class="meta">No concepts recorded yet. Add them to the paper YAML, then rebuild.</p>'
    centre_x, centre_y, radius = 320, 220, 150
    points = {}
    for index, node in enumerate(nodes):
        angle = (2 * math.pi * index / len(nodes)) - (math.pi / 2)
        points[node["id"]] = (
            round(centre_x + radius * math.cos(angle), 1),
            round(centre_y + radius * math.sin(angle), 1),
        )
    parts = ['<svg viewBox="0 0 640 440" role="img" aria-label="Concept map">']
    for link in graph["links"]:
        if link["source"] in points and link["target"] in points:
            x1, y1 = points[link["source"]]
            x2, y2 = points[link["target"]]
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888" stroke-width="1.5"/>')
    for node in nodes:
        x, y = points[node["id"]]
        size = 12 + min(int(node.get("mentions") or 0), 10)
        label = node["label"][:24] + ("…" if len(node["label"]) > 24 else "")
        parts.append(f'<circle cx="{x}" cy="{y}" r="{size}" fill="#3a7" stroke="#263" />')
        parts.append(f'<text x="{x}" y="{y + size + 15}" text-anchor="middle" font-size="12">{esc(label)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def concept_page(topic: str, paper: dict[str, Any]) -> str:
    graph = concept_graph(paper)
    title = text(paper.get("title")) or topic
    parts = [f"<h1>{esc(title)}</h1>", f'<p class="meta">Source: papers/content/arxiv-{esc(topic)}.yaml</p>']
    if text(paper.get("abstract")):
        parts += ["<h2>Abstract</h2>", f"<p>{esc(text(paper.get('abstract')))}</p>"]
    parts += ["<h2>Concept map</h2>", concept_svg(graph)]
    if graph["nodes"]:
        parts += ["<h2>Concepts</h2>", "<table><tr><th>Concept</th><th>Definition</th></tr>"]
        parts += [
            f"<tr><td>{esc(node['label'])}</td><td>{esc(node['definition'])}</td></tr>" for node in graph["nodes"]
        ]
        parts.append("</table>")
    equations = items(paper.get("equations"))
    if equations:
        parts += ["<h2>Equations</h2>"]
        for equation in equations:
            parts += [
                f"<h3>{esc(text(equation.get('id')) or 'equation')}</h3>",
                f"<pre><code>{esc(text(equation.get('latex')))}</code></pre>",
                f"<p>{esc(text(equation.get('description')))}</p>",
            ]
    claims = items(paper.get("claims"))
    if claims:
        parts += ["<h2>Claims to defend</h2>"]
        parts += [f"<p>{esc(text(claim.get('text')))}</p>" for claim in claims]
    source = paper.get("source")
    if isinstance(source, dict) and source.get("paper_id"):
        parts += [
            "<h2>Source</h2>",
            f'<p class="meta">{esc(source.get("paper_id"))} · {esc(source.get("licence"))}</p>',
        ]
    return page(title, "\n".join(parts), section=True)


def proof_depths(proof: dict[str, Any]) -> dict[str, int]:
    """Layer a proof DAG; a cycle is a content error, not a rendering quirk."""
    steps = items(proof.get("steps"))
    ids = [text(step.get("id")) or f"step-{index}" for index, step in enumerate(steps, start=1)]
    if len(ids) != len(set(ids)):
        raise ContentError(f"{text(proof.get('id'))}: step ids must be unique")
    known = set(ids)
    depths: dict[str, int] = {}
    for step_id, step in zip(ids, steps, strict=True):
        deps = [text(value) for value in step.get("depends_on", []) if text(value)]
        unknown = [dep for dep in deps if dep not in known]
        if unknown:
            raise ContentError(f"{text(proof.get('id'))}: {step_id} depends on unknown steps {unknown}")
        depths[step_id] = 0
    for _ in range(len(ids)):
        changed = False
        for step_id, step in zip(ids, steps, strict=True):
            deps = [text(value) for value in step.get("depends_on", []) if text(value)]
            if deps:
                candidate = max(depths[dep] for dep in deps) + 1
                if candidate > depths[step_id]:
                    depths[step_id] = candidate
                    changed = True
        if not changed:
            return depths
    raise ContentError(f"{text(proof.get('id'))}: step dependencies contain a cycle")


def proof_svg(proof: dict[str, Any]) -> str:
    steps = items(proof.get("steps"))
    if not steps:
        return '<p class="meta">No proof steps recorded yet.</p>'
    depths = proof_depths(proof)
    ids = [text(step.get("id")) or f"step-{index}" for index, step in enumerate(steps, start=1)]
    layers: dict[int, list[str]] = {}
    for step_id in ids:
        layers.setdefault(depths[step_id], []).append(step_id)
    points = {}
    for depth, members in sorted(layers.items()):
        for index, step_id in enumerate(members, start=1):
            points[step_id] = (100 + depth * 210, 60 + index * 110)
    max_depth = max(depths.values())
    height = 120 + max(len(members) for members in layers.values()) * 110
    parts = [
        f'<svg viewBox="0 0 {140 + max_depth * 210 + 160} {height}" role="img" aria-label="Proof dependency graph">',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
        '<path d="M0,0 L0,6 L7,3 z" fill="#666"/></marker></defs>',
    ]
    for step_id, step in zip(ids, steps, strict=True):
        x, y = points[step_id]
        for dep in [text(value) for value in step.get("depends_on", []) if text(value)]:
            x1, y1 = points[dep]
            parts.append(
                f'<line x1="{x1 + 90}" y1="{y1}" x2="{x - 95}" y2="{y}" stroke="#666" '
                'stroke-width="1.5" marker-end="url(#arrow)"/>'
            )
    for step_id, step in zip(ids, steps, strict=True):
        x, y = points[step_id]
        label = text(step.get("label")) or step_id
        parts.append(f'<rect x="{x - 90}" y="{y - 25}" width="180" height="50" rx="8" fill="#3a7" stroke="#263"/>')
        parts.append(
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" fill="#fff" font-size="13">{esc(label[:26])}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def proof_page(topic: str, proof: dict[str, Any]) -> str:
    title = text(proof.get("title")) or topic
    parts = [f"<h1>{esc(title)}</h1>"]
    if text(proof.get("statement")):
        parts += ["<h2>Statement</h2>", f"<p>{esc(text(proof.get('statement')))}</p>"]
    if text(proof.get("invariant")):
        parts += ["<h2>Invariant</h2>", f"<p>{esc(text(proof.get('invariant')))}</p>"]
    parts += ["<h2>Proof graph</h2>", proof_svg(proof)]
    steps = items(proof.get("steps"))
    if steps:
        parts += ["<h2>Steps</h2>", "<table><tr><th>Step</th><th>Detail</th><th>Depends on</th></tr>"]
        parts += [
            f"<tr><td>{esc(text(step.get('label')) or text(step.get('id')))}</td>"
            f"<td>{esc(text(step.get('detail')))}</td>"
            f"<td>{esc(', '.join(text(value) for value in step.get('depends_on', [])))}</td></tr>"
            for step in steps
        ]
        parts.append("</table>")
    if text(proof.get("complexity")):
        parts += ["<h2>Complexity</h2>", f"<p>{esc(text(proof.get('complexity')))}</p>"]
    return page(title, "\n".join(parts), section=True)


def diagrams_html(patterns: list[dict[str, Any]], root: Path = REPO_ROOT) -> str:
    parts = ["<h1>Architecture diagrams</h1>", '<p class="meta">Original SVGs from data/patterns.json.</p>']
    for pattern in patterns:
        diagram = pattern.get("diagram")
        if not isinstance(diagram, dict):
            continue
        relative = text(diagram.get("file"))
        if not relative:
            continue
        if not (root / relative).is_file():
            raise ContentError(f"{text(pattern.get('id'))}: diagram file missing: {relative}")
        parts += [
            "<figure>",
            f'<img src="../../{esc(relative)}" alt="{esc(text(diagram.get("alt")))}">',
            f"<figcaption><strong>{esc(text(pattern.get('title')))}</strong> — "
            f"{esc(text(pattern.get('decision'))[:180])}</figcaption>",
            "</figure>",
        ]
    return page("Architecture diagrams", "\n".join(parts), section=True)


def render_all(root: Path = REPO_ROOT) -> dict[Path, str]:
    papers = load_papers(root)
    patterns = load_patterns(root)
    proofs = load_proofs(root)
    outputs: dict[Path, str] = {}
    for topic, paper in papers:
        outputs[Path(f"concepts/arxiv-{topic}.html")] = concept_page(topic, paper)
    outputs[Path("concepts/index.html")] = page(
        "Concept maps",
        "\n".join(
            ["<h1>Concept maps</h1>"]
            + [
                f'<p><a href="arxiv-{esc(topic)}.html">{esc(text(paper.get("title")) or topic)}</a></p>'
                for topic, paper in papers
            ]
        ),
        section=True,
    )
    outputs[Path("diagrams/index.html")] = diagrams_html(patterns, root)
    proof_links = []
    for topic, proof in proofs:
        outputs[Path(f"proofs/{topic}.html")] = proof_page(topic, proof)
        proof_links.append(f'<p><a href="{esc(topic)}.html">{esc(text(proof.get("title")) or topic)}</a></p>')
    outputs[Path("proofs/index.html")] = page(
        "Proof graphs",
        "\n".join(
            ["<h1>Proof graphs</h1>"]
            + (
                proof_links
                or ['<p class="meta">No proof YAML yet. The renderer is ready; add proofs/content/*.yaml.</p>']
            )
        ),
        section=True,
    )
    outputs[Path("index.html")] = page(
        "Visual review",
        "\n".join(
            [
                "<h1>Visual review</h1>",
                '<p class="meta">Generated from committed content. No network requests, no external scripts.</p>',
                '<div class="grid">',
                '<div><h2><a href="../cards/index.html">Cards</a></h2><p>Timed mixed review with local scheduling.</p></div>',
                f'<div><h2><a href="concepts/index.html">Concept maps</a></h2><p>{len(papers)} paper map(s).</p></div>',
                f'<div><h2><a href="diagrams/index.html">Diagrams</a></h2><p>{len(patterns)} architecture diagram(s).</p></div>',
                f'<div><h2><a href="proofs/index.html">Proof graphs</a></h2><p>{len(proofs)} proof DAG(s).</p></div>',
                "</div>",
            ]
        ),
    )
    outputs[Path("sources.json")] = (
        json.dumps(
            {
                "papers": [topic for topic, _ in papers],
                "patterns": [text(pattern.get("id")) for pattern in patterns],
                "proofs": [topic for topic, _ in proofs],
            },
            indent=2,
        )
        + "\n"
    )
    return outputs


def write_all(root: Path = ROOT) -> list[Path]:
    written = []
    for relative, text_value in render_all().items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        _ = target.write_text(text_value, encoding="utf-8")
        written.append(target)
    return written


app = typer.Typer(help="Render deterministic visual review pages from committed content.")


@app.command()
def build(check: bool = typer.Option(False, "--check", help="Fail when a checked-in output differs.")) -> None:
    """Regenerate the visual hub, concept maps, diagram gallery, and proof graphs."""
    outputs = render_all()
    if check:
        stale = [
            relative.as_posix()
            for relative, text_value in outputs.items()
            if not (ROOT / relative).exists() or (ROOT / relative).read_text(encoding="utf-8") != text_value
        ]
        if stale:
            typer.echo(f"Stale visual outputs (run the builder): {', '.join(stale)}", err=True)
            raise typer.Exit(1)
        typer.echo(f"Visual outputs current ({len(outputs)} files).")
        return
    for path in write_all():
        typer.echo(f"wrote {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    app()
