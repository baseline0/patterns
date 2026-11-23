"""Generate deterministic study artifacts for object and application design patterns.

Source of truth: content/*.yaml. Outputs: per-pattern README, quiz guide, self-contained HTML, glossary cards, and a
family index. No network, no sibling imports.
"""

from __future__ import annotations

import csv
import html
import io
import json
from pathlib import Path
from typing import Any

import typer
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
REQUIRED = (
    "id",
    "name",
    "category",
    "intent",
    "problem",
    "structure",
    "participants",
    "forces",
    "consequences",
    "smells_fixed",
    "smells_created",
    "python",
    "example",
    "related_architecture",
    "quiz",
)


class ContentError(ValueError):
    """A pattern file is missing a required part or has an inconsistent quiz."""


def load_patterns(content_dir: Path = CONTENT) -> list[dict[str, Any]]:
    patterns = []
    for path in sorted(content_dir.glob("*.yaml")):
        pattern = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(pattern, dict):
            raise ContentError(f"{path.name}: expected a YAML mapping")
        validate(pattern, source=path.name)
        patterns.append(pattern)
    if not patterns:
        raise ContentError(f"no pattern files in {content_dir}")
    return patterns


def validate(pattern: dict[str, Any], source: str) -> None:
    missing = [key for key in REQUIRED if key not in pattern]
    if missing:
        raise ContentError(f"{source}: missing {', '.join(missing)}")
    if not isinstance(pattern["participants"], list) or len(pattern["participants"]) < 2:
        raise ContentError(f"{source}: participants needs at least two roles")
    if not isinstance(pattern["related_architecture"], list) or not pattern["related_architecture"]:
        raise ContentError(f"{source}: related_architecture cannot be empty")
    quiz = pattern["quiz"]
    if not isinstance(quiz, list) or len(quiz) < 2:
        raise ContentError(f"{source}: quiz needs at least two questions")
    for index, item in enumerate(quiz):
        choices = item.get("choices", [])
        if not 0 <= item.get("answer", -1) < len(choices):
            raise ContentError(f"{source}: quiz item {index} has an answer outside its choices")


def readme(pattern: dict[str, Any]) -> str:
    lines = [
        f"# {pattern['name']}",
        "",
        "> Generated from `content/`. Edit the YAML, then run `tools/build.py`.",
        "",
        "- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`",
        "",
        f"**Category**: {pattern['category']}",
        "",
        f"**Intent**: {pattern['intent']}",
        "",
        "## Problem",
        "",
        str(pattern["problem"]).strip(),
        "",
        "## Structure",
        "",
        "```text",
        str(pattern["structure"]).strip(),
        "```",
        "",
        "## Participants",
        "",
    ]
    for role in pattern["participants"]:
        lines.append(f"- **{role['name']}**: {role['role']}")
    lines += ["", "## Forces", ""]
    lines += [f"- {force}" for force in pattern["forces"]]
    lines += [
        "",
        "## Consequences",
        "",
        f"- **Benefit**: {pattern['consequences']['benefit']}",
        f"- **Cost**: {pattern['consequences']['cost']}",
        "",
        "## Smells",
        "",
        f"- Fixed: {', '.join(pattern['smells_fixed'])}",
        f"- Created: {', '.join(pattern['smells_created'])}",
        "",
        "## Python sketch",
        "",
        "```python",
        str(pattern["python"]).strip(),
        "```",
        "",
        "## Interview example",
        "",
        str(pattern["example"]).strip(),
        "",
        "## Related architecture patterns",
        "",
    ]
    lines += [f"- `{item}`" for item in pattern["related_architecture"]]
    if pattern.get("catalog_refs"):
        lines += ["", "## Catalog subjects", ""]
        lines += [f"- `{ref}`" for ref in pattern["catalog_refs"]]
    return "\n".join(lines).rstrip("\n") + "\n"


def quiz_guide(pattern: dict[str, Any]) -> str:
    lines = [f"# Quiz: {pattern['name']}", "", "> Generated from `content/`.", ""]
    for number, item in enumerate(pattern["quiz"], start=1):
        lines += [f"## {number}. {item['question']}", ""]
        lines += [f"{letter}. {choice}" for letter, choice in zip("ABCDEFGH", item["choices"], strict=False)]
        lines += ["", f"**Answer: {'ABCDEFGH'[item['answer']]}.** {item['explanation']}", ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def index_html(pattern: dict[str, Any]) -> str:
    esc = html.escape
    parts = [
        "<!doctype html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(pattern['name'])}</title>",
        "<style>body{font-family:system-ui,sans-serif;max-width:52rem;margin:2rem auto;padding:0 1rem;line-height:1.5}"
        "pre{background:#f3f3f3;padding:1rem;overflow-x:auto}code{background:#f3f3f3;padding:0 .2rem}nav a{margin-right:1rem}</style>",
        "</head><body>",
        '<nav><a href="../../site/index.html">Explorer</a><a href="../../visual/index.html">Visual hub</a><a href="../../cards/index.html">Cards</a><a href="../INDEX.md">Index</a></nav>',
        f"<h1>{esc(pattern['name'])}</h1>",
        f"<p><strong>{esc(pattern['category'])}</strong> — {esc(pattern['intent'])}</p>",
        f"<h2>Problem</h2><p>{esc(pattern['problem'])}</p>",
        f"<h2>Structure</h2><pre>{esc(pattern['structure'])}</pre>",
        "<h2>Participants</h2><ul>",
    ]
    parts += [f"<li><strong>{esc(r['name'])}</strong>: {esc(r['role'])}</li>" for r in pattern["participants"]]
    parts += ["</ul><h2>Forces</h2><ul"]
    parts += [f"><li>{esc(f)}</li>" for f in pattern["forces"]]
    parts += [
        "></ul>",
        f"<h2>Consequences</h2><p><strong>Benefit:</strong> {esc(pattern['consequences']['benefit'])}</p>",
        f"<p><strong>Cost:</strong> {esc(pattern['consequences']['cost'])}</p>",
        f"<h2>Python sketch</h2><pre>{esc(pattern['python'])}</pre>",
        f"<h2>Interview example</h2><p>{esc(pattern['example'])}</p>",
    ]
    refs = pattern.get("catalog_refs", [])
    if refs:
        parts += ["<h2>Catalog subjects</h2><ul>"]
        parts += [f"<li><code>{esc(ref)}</code></li>" for ref in refs]
        parts += ["</ul>"]
    return "\n".join(parts) + "\n</body></html>\n"


def glossary_cards(pattern: dict[str, Any]) -> list[dict[str, Any]]:
    pattern_id = pattern["id"]
    tags = ["design-pattern", pattern["category"], pattern_id]
    cards = [
        {
            "title": f"Intent: {pattern['name']}",
            "body": pattern["intent"],
            "metadata": {"tags": [*tags, "intent"], "source": "design-patterns/glossary.json"},
        },
        {
            "title": f"Use {pattern['name']} when",
            "body": pattern["problem"],
            "metadata": {"tags": [*tags, "problem"], "source": "design-patterns/glossary.json"},
        },
        {
            "title": f"Trade-off: {pattern['name']}",
            "body": f"**Benefit**: {pattern['consequences']['benefit']}\n\n**Cost**: {pattern['consequences']['cost']}",
            "metadata": {"tags": [*tags, "tradeoff"], "source": "design-patterns/glossary.json"},
        },
    ]
    for index, item in enumerate(pattern["quiz"], start=1):
        choices = "\n".join(f"{letter}. {choice}" for letter, choice in zip("ABCDEFGH", item["choices"], strict=False))
        body = f"{choices}\n\n**{'ABCDEFGH'[item['answer']]}.** {item['explanation']}"
        cards.append(
            {
                "title": f"Q{index}: {item['question'][:60]}",
                "body": body,
                "metadata": {"tags": [*tags, "question"], "source": "design-patterns/glossary.json"},
            }
        )
    return cards


def family_glossary(patterns: list[dict[str, Any]]) -> str:
    cards = [card for pattern in patterns for card in glossary_cards(pattern)]
    return json.dumps(cards, indent=2, ensure_ascii=False) + "\n"


def flashcards(patterns: list[dict[str, Any]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    for pattern in patterns:
        for item in pattern["quiz"]:
            answer = item["choices"][item["answer"]]
            writer.writerow([item["question"], f"{answer}. {item['explanation']}", f"design-pattern {pattern['id']}"])
    return buffer.getvalue()


def family_readme(patterns: list[dict[str, Any]]) -> str:
    lines = [
        "# Design patterns",
        "",
        "> Generated from `content/`. Edit the YAML, then run `tools/build.py`.",
        "",
        "Object and application patterns are the bridge between data-structure reasoning and system architecture.",
        "",
        "## Patterns",
        "",
    ]
    for pattern in patterns:
        lines.append(f"- [{pattern['name']}]({pattern['id']}/README.md) — {pattern['category']}: {pattern['intent']}")
    lines += [
        "",
        "## Explore",
        "",
        "- Searchable local catalogue: `just -f site/justfile serve` then open `site/index.html`.",
        "",
        "## Use it",
        "",
        "- `just -f design-patterns/justfile build`",
        "- `just -f design-patterns/justfile check`",
        "- `just -f design-patterns/justfile quiz`",
        "",
        "Cards feed `cards/deck.json` from `design-patterns/glossary.json`.",
    ]
    return "\n".join(lines).rstrip("\n") + "\n"


def render_all(content_dir: Path = CONTENT) -> dict[Path, str]:
    patterns = load_patterns(content_dir)
    outputs: dict[Path, str] = {}
    for pattern in patterns:
        stem = Path(pattern["id"])
        outputs[stem / "README.md"] = readme(pattern)
        outputs[stem / "quiz_guide.md"] = quiz_guide(pattern)
        outputs[stem / "index.html"] = index_html(pattern)
    outputs[Path("glossary.json")] = family_glossary(patterns)
    outputs[Path("flashcards.csv")] = flashcards(patterns)
    outputs[Path("INDEX.md")] = family_readme(patterns)
    return outputs


def write_all(root: Path = ROOT) -> list[Path]:
    written = []
    for relative, value in render_all().items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        _ = target.write_text(value, encoding="utf-8")
        written.append(target)
    return written


app = typer.Typer(help="Build deterministic design-pattern study artifacts.")


@app.command()
def build(check: bool = typer.Option(False, "--check", help="Fail when a checked-in output differs.")) -> None:
    """Regenerate design-pattern notes, quizzes, and cards from committed YAML."""
    outputs = render_all()
    if check:
        stale = [
            path.as_posix()
            for path, value in outputs.items()
            if not (ROOT / path).exists() or (ROOT / path).read_text(encoding="utf-8") != value
        ]
        if stale:
            typer.echo(f"Stale design-pattern outputs: {', '.join(stale)}", err=True)
            raise typer.Exit(1)
        typer.echo(f"Design-pattern outputs current ({len(outputs)} files).")
        return
    for path in write_all():
        typer.echo(f"wrote {path.relative_to(ROOT.parent)}")


@app.command()
def quiz(category: str | None = typer.Option(None, "--category", help="Limit to one category.")) -> None:
    """Run a short terminal quiz from the committed pattern YAML."""
    patterns = [p for p in load_patterns() if category is None or p["category"] == category]
    if not patterns:
        typer.echo("No patterns match that category.", err=True)
        raise typer.Exit(1)
    score = 0
    total = 0
    for pattern in patterns:
        for item in pattern["quiz"]:
            total += 1
            typer.echo(f"\n{pattern['name']}: {item['question']}")
            for letter, choice in zip("ABCDEFGH", item["choices"], strict=False):
                typer.echo(f"  {letter}. {choice}")
            answer = typer.prompt("Answer", default="A").strip().upper()
            if answer == "ABCDEFGH"[item["answer"]]:
                score += 1
                typer.echo("correct")
            else:
                typer.echo(f"{item['explanation']}")
    typer.echo(f"\nScore: {score}/{total}")


@app.command("list")
def list_patterns() -> None:
    """List pattern ids and categories."""
    for pattern in load_patterns():
        typer.echo(f"{pattern['id']:24} {pattern['category']:14} {pattern['name']}")


if __name__ == "__main__":
    app()
