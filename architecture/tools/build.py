"""Build the canonical architecture catalogue, graph, and review cards from committed YAML.

Sources: content/catalogue.yaml plus content/styles, content/tactics, and content/quality-attributes. No network and no
sibling-runtime imports.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import typer
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
REPO_ROOT = ROOT.parent
KINDS = {
    "styles": (
        "id",
        "name",
        "summary",
        "decision",
        "use_when",
        "avoid_when",
        "components",
        "tradeoffs",
        "quality_impacts",
        "related_patterns",
        "scenarios",
        "quiz",
    ),
    "tactics": (
        "id",
        "name",
        "summary",
        "mechanism",
        "failure_modes",
        "use_when",
        "avoid_when",
        "tradeoffs",
        "quality_impacts",
        "related_patterns",
        "scenarios",
        "quiz",
    ),
    "quality-attributes": (
        "id",
        "name",
        "definition",
        "stimulus",
        "response",
        "measure",
        "tactics",
        "related_patterns",
        "quiz",
    ),
}


class ContentError(ValueError):
    """A catalogue or architecture source is missing a required part."""


def load_catalogue(path: Path = CONTENT / "catalogue.yaml") -> dict[str, Any]:
    catalogue = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(catalogue, dict) or "scenarios" not in catalogue:
        raise ContentError("catalogue.yaml needs a scenarios list")
    for scenario in catalogue["scenarios"]:
        for key in ("id", "title", "status"):
            if key not in scenario:
                raise ContentError(f"catalogue scenario missing {key}")
    return catalogue


def load_kind(kind: str, content_dir: Path = CONTENT) -> list[dict[str, Any]]:
    required = KINDS[kind]
    items = []
    for path in sorted((content_dir / kind).glob("*.yaml")):
        item = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(item, dict):
            raise ContentError(f"{path.name}: expected a YAML mapping")
        missing = [key for key in required if key not in item]
        if missing:
            raise ContentError(f"{path.name}: missing {', '.join(missing)}")
        for index, question in enumerate(item.get("quiz", [])):
            choices = question.get("choices", [])
            if not 0 <= question.get("answer", -1) < len(choices):
                raise ContentError(f"{path.name}: quiz item {index} has an answer outside its choices")
        items.append(item)
    if not items:
        raise ContentError(f"no files in {content_dir / kind}")
    return items


def load_all(content_dir: Path = CONTENT) -> dict[str, list[dict[str, Any]]]:
    return {kind: load_kind(kind, content_dir) for kind in KINDS}


def load_design_patterns(directory: Path | None = None) -> list[dict[str, Any]]:
    directory = directory or REPO_ROOT / "design-patterns" / "content"
    patterns = []
    for path in sorted(directory.glob("*.yaml")):
        item = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(item, dict) or not all(key in item for key in ("id", "name", "category")):
            raise ContentError(f"{path.name}: incomplete design pattern")
        patterns.append(item)
    return patterns


def ids_by_kind(items: dict[str, list[dict[str, Any]]]) -> dict[str, set[str]]:
    return {kind: {item["id"] for item in group} for kind, group in items.items()}


def validate_references(catalogue: dict[str, Any], items: dict[str, list[dict[str, Any]]]) -> None:
    known = ids_by_kind(items)
    all_patterns = (
        known["styles"]
        | known["tactics"]
        | known["quality-attributes"]
        | {item["id"] for item in load_design_patterns()}
    )
    scenario_ids = {scenario["id"] for scenario in catalogue["scenarios"]}
    seen: set[str] = set()
    for kind, group in items.items():
        for item in group:
            if item["id"] in seen:
                raise ContentError(f"duplicate architecture id: {item['id']}")
            seen.add(item["id"])
            for related in item.get("related_patterns", []):
                if related not in all_patterns | scenario_ids:
                    raise ContentError(f"{item['id']}: related target {related} does not resolve")
            for scenario in item.get("scenarios", []):
                if scenario not in scenario_ids:
                    raise ContentError(f"{item['id']}: scenario {scenario} does not resolve")
            for impact in item.get("quality_impacts", []):
                if impact["attribute"] not in known["quality-attributes"]:
                    raise ContentError(f"{item['id']}: quality attribute {impact['attribute']} does not resolve")
    for pattern in load_design_patterns():
        for target in pattern.get("related_architecture", []):
            if target not in all_patterns | scenario_ids:
                raise ContentError(f"design pattern {pattern['id']}: related architecture {target} does not resolve")
    for scenario in catalogue["scenarios"]:
        for key in ("path", "hints", "solution", "rubric"):
            location = scenario.get(key)
            if not location or not (REPO_ROOT / location).is_file():
                raise ContentError(f"scenario {scenario['id']}: missing {key} at {location}")


def cards(items: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for kind, group in items.items():
        for item in group:
            label = "quality attribute" if kind == "quality-attributes" else kind[:-1]
            tags = ["architecture", label, item["id"], *item.get("scenarios", [])]
            source = "architecture/glossary.json"
            result.append(
                {
                    "title": f"{item['name']}: definition",
                    "body": item.get("definition") or item["summary"],
                    "metadata": {"tags": [*tags, "definition"], "source": source},
                }
            )
            if item.get("decision") or item.get("mechanism"):
                result.append(
                    {
                        "title": f"{item['name']}: decision",
                        "body": item.get("decision") or item["mechanism"],
                        "metadata": {"tags": [*tags, "decision"], "source": source},
                    }
                )
            for tradeoff in item.get("tradeoffs", []):
                result.append(
                    {
                        "title": f"Trade-off: {item['name']}",
                        "body": f"**Benefit**: {tradeoff['benefit']}\n\n**Cost**: {tradeoff['cost']}",
                        "metadata": {"tags": [*tags, "tradeoff"], "source": source},
                    }
                )
            for impact in item.get("quality_impacts", []):
                result.append(
                    {
                        "title": f"Quality impact: {item['name']} / {impact['attribute']}",
                        "body": f"**{impact['effect']}**: {impact['note']}",
                        "metadata": {"tags": [*tags, "quality-attribute", impact["attribute"]], "source": source},
                    }
                )
            for index, question in enumerate(item.get("quiz", []), start=1):
                choices = "\n".join(
                    f"{letter}. {choice}" for letter, choice in zip("ABCDEFGH", question["choices"], strict=False)
                )
                answer = f"**{'ABCDEFGH'[question['answer']]}.** {question['explanation']}"
                result.append(
                    {
                        "title": f"Q{index}: {question['question'][:60]}",
                        "body": f"{choices}\n\n{answer}",
                        "metadata": {"tags": [*tags, "question"], "source": source},
                    }
                )
    return result


def graph(catalogue: dict[str, Any], items: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    design_patterns = load_design_patterns()
    nodes = [{"id": item["id"], "kind": kind, "label": item["name"]} for kind, group in items.items() for item in group]
    nodes += [{"id": item["id"], "kind": "design-pattern", "label": item["name"]} for item in design_patterns]
    nodes += [
        {"id": scenario["id"], "kind": "scenario", "label": scenario["title"]} for scenario in catalogue["scenarios"]
    ]
    links: list[dict[str, str]] = []
    for kind, group in items.items():
        for item in group:
            for related in item.get("related_patterns", []):
                links.append({"source": item["id"], "target": related, "kind": "related"})
            for scenario in item.get("scenarios", []):
                links.append({"source": item["id"], "target": scenario, "kind": "scenario"})
            for impact in item.get("quality_impacts", []):
                links.append({"source": item["id"], "target": impact["attribute"], "kind": impact["effect"]})
    for pattern in design_patterns:
        for target in pattern.get("related_architecture", []):
            links.append({"source": pattern["id"], "target": target, "kind": "applies-to"})
    for scenario in catalogue["scenarios"]:
        for pattern in scenario.get("patterns", []):
            links.append({"source": scenario["id"], "target": pattern, "kind": "uses"})
    return {"nodes": nodes, "links": links}


def catalogue_markdown(catalogue: dict[str, Any], items: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# Architecture catalogue",
        "",
        "> Generated from `architecture/content/catalogue.yaml`. Edit YAML, then run `tools/build.py`.",
        "",
        "This is the canonical index for design patterns, architecture styles, tactics, quality attributes, and scenarios.",
        "",
        "## Families",
        "",
    ]
    for kind in KINDS:
        lines += [f"### {kind.replace('-', ' ').title()} ({len(items[kind])})", ""]
        lines += [f"- `{item['id']}` — {item['name']}" for item in items[kind]]
        lines.append("")
    lines += [
        "## Scenarios",
        "",
        "| ID | Title | Status | Prompt | Solution | Rubric |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for scenario in catalogue["scenarios"]:
        lines.append(
            f"| `{scenario['id']}` | {scenario['title']} | {scenario['status']} "
            f"| [README](../{scenario['path']}) | [SOLUTION](../{scenario['solution']}) | [RUBRIC](../{scenario['rubric']}) |"
        )
    return "\n".join(lines).rstrip("\n") + "\n"


def catalogue_html(catalogue: dict[str, Any], items: dict[str, list[dict[str, Any]]]) -> str:
    esc = html.escape
    parts = [
        "<!doctype html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Architecture catalogue</title>",
        "<style>body{font-family:system-ui,sans-serif;max-width:60rem;margin:2rem auto;padding:0 1rem;line-height:1.5}"
        "li{margin:.25rem 0}code{background:#f3f3f3;padding:0 .2rem}</style>",
        "</head><body>",
        "<h1>Architecture catalogue</h1>",
        "<p>Canonical index generated from committed YAML.</p>",
    ]
    for kind in KINDS:
        parts.append(f"<h2>{esc(kind.replace('-', ' ').title())}</h2><ul>")
        parts += [f"<li><code>{esc(item['id'])}</code> — {esc(item['name'])}</li>" for item in items[kind]]
        parts.append("</ul>")
    parts.append("<h2>Scenarios</h2><ul>")
    parts += [
        f"<li><code>{esc(s['id'])}</code> — {esc(s['title'])} ({esc(s['status'])})</li>" for s in catalogue["scenarios"]
    ]
    parts.append("</ul></body></html>")
    return "\n".join(parts) + "\n"


def render_all(content_dir: Path = CONTENT) -> dict[Path, str]:
    catalogue = load_catalogue(content_dir / "catalogue.yaml")
    items = load_all(content_dir)
    validate_references(catalogue, items)
    return {
        Path("CATALOGUE.md"): catalogue_markdown(catalogue, items),
        Path("catalogue.json"): json.dumps({"catalogue": catalogue, **items}, indent=2, ensure_ascii=False) + "\n",
        Path("glossary.json"): json.dumps(cards(items), indent=2, ensure_ascii=False) + "\n",
        Path("graph.json"): json.dumps(graph(catalogue, items), indent=2, ensure_ascii=False) + "\n",
        Path("index.html"): catalogue_html(catalogue, items),
    }


def write_all(root: Path = ROOT) -> list[Path]:
    written = []
    for relative, value in render_all().items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        _ = target.write_text(value, encoding="utf-8")
        written.append(target)
    return written


app = typer.Typer(help="Build the canonical architecture catalogue and cards.")


@app.command()
def build(check: bool = typer.Option(False, "--check", help="Fail when a checked-in output differs.")) -> None:
    """Regenerate catalogue, graph, and glossary from committed architecture YAML."""
    outputs = render_all()
    if check:
        stale = [
            path.as_posix()
            for path, value in outputs.items()
            if not (ROOT / path).exists() or (ROOT / path).read_text(encoding="utf-8") != value
        ]
        if stale:
            typer.echo(f"Stale architecture outputs: {', '.join(stale)}", err=True)
            raise typer.Exit(1)
        typer.echo(f"Architecture outputs current ({len(outputs)} files).")
        return
    for path in write_all():
        typer.echo(f"wrote {path.relative_to(ROOT.parent)}")


@app.command()
def list() -> None:
    """List architecture ids by kind."""
    for kind, group in load_all().items():
        for item in group:
            typer.echo(f"{kind:20} {item['id']:28} {item['name']}")


if __name__ == "__main__":
    app()
