"""Build the cross-provider mapping matrix and review cards from committed YAML.

Sources: content/*.yaml. Each mapping names an offline Terraform fixture under terraform/<provider>/<pattern>.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import typer
import yaml

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent
CONTENT = ROOT / "content"
PROVIDERS = ("aws", "azure", "gcp")


class ContentError(ValueError):
    """A provider mapping is missing a required field or fixture."""


def load_mappings(content_dir: Path = CONTENT) -> list[dict[str, Any]]:
    mappings = []
    for path in sorted(content_dir.glob("*.yaml")):
        mapping = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(mapping, dict):
            raise ContentError(f"{path.name}: expected a YAML mapping")
        for key in ("id", "name", "summary", "providers", "quiz"):
            if key not in mapping:
                raise ContentError(f"{path.name}: missing {key}")
        for provider in PROVIDERS:
            entry = mapping["providers"].get(provider)
            if not entry or not entry.get("plan_fixture"):
                raise ContentError(f"{path.name}: missing {provider} plan_fixture")
            if not (REPO_ROOT / entry["plan_fixture"]).is_dir():
                raise ContentError(f"{path.name}: {provider} fixture missing at {entry['plan_fixture']}")
        for index, question in enumerate(mapping["quiz"]):
            choices = question.get("choices", [])
            if not 0 <= question.get("answer", -1) < len(choices):
                raise ContentError(f"{path.name}: quiz item {index} has an answer outside its choices")
        mappings.append(mapping)
    if not mappings:
        raise ContentError("no provider mappings found")
    return mappings


def cards(mappings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for mapping in mappings:
        tags = ["provider", mapping["id"]]
        result.append(
            {
                "title": f"Provider map: {mapping['name']}",
                "body": "\n".join(f"**{p}**: {mapping['providers'][p]['services']}" for p in PROVIDERS),
                "metadata": {"tags": [*tags, "mapping"], "source": "providers/glossary.json"},
            }
        )
        for provider in PROVIDERS:
            entry = mapping["providers"][provider]
            result.append(
                {
                    "title": f"{mapping['name']} on {provider.upper()}",
                    "body": f"{entry['services']}\n\n**Plan only**: `{entry['plan_fixture']}`\n\n**Watch out**: {entry['watch_out']}",
                    "metadata": {"tags": [*tags, provider], "source": "providers/glossary.json"},
                }
            )
        for index, question in enumerate(mapping["quiz"], start=1):
            choices = "\n".join(
                f"{letter}. {choice}" for letter, choice in zip("ABCDEFGH", question["choices"], strict=False)
            )
            answer = f"**{'ABCDEFGH'[question['answer']]}.** {question['explanation']}"
            result.append(
                {
                    "title": f"Q{index}: {question['question'][:60]}",
                    "body": f"{choices}\n\n{answer}",
                    "metadata": {"tags": [*tags, "question"], "source": "providers/glossary.json"},
                }
            )
    return result


def matrix_markdown(mappings: list[dict[str, Any]]) -> str:
    lines = [
        "# Provider mappings",
        "",
        "> Generated from `content/`. Edit YAML, then run `tools/build.py`.",
        "",
        "Vendor-agnostic pattern first; provider details second. Every fixture is `terraform plan`-only.",
        "",
    ]
    for mapping in mappings:
        lines += [f"## {mapping['name']}", "", mapping["summary"], ""]
        lines += ["| Provider | Services | Emulator | Fixture | Watch out |", "| --- | --- | --- | --- | --- |"]
        for provider in PROVIDERS:
            entry = mapping["providers"][provider]
            lines.append(
                f"| {provider.upper()} | {entry['services']} | {entry['emulator']} "
                f"| `{entry['plan_fixture']}` | {entry['watch_out']} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def matrix_html(mappings: list[dict[str, Any]]) -> str:
    esc = html.escape
    parts = [
        "<!doctype html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Provider mappings</title>",
        "<style>body{font-family:system-ui,sans-serif;max-width:60rem;margin:2rem auto;padding:0 1rem;line-height:1.5}"
        "table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:.4rem;text-align:left;vertical-align:top}</style>",
        "</head><body>",
        "<h1>Provider mappings</h1>",
    ]
    for mapping in mappings:
        parts += [f"<h2>{esc(mapping['name'])}</h2>", f"<p>{esc(mapping['summary'])}</p>", "<table><tr>"]
        parts += [f"<th>{p.upper()}</th>" for p in PROVIDERS]
        parts.append("</tr><tr>")
        parts += [f"<td>{esc(mapping['providers'][p]['services'])}</td>" for p in PROVIDERS]
        parts.append("</tr></table>")
    parts.append("</body></html>")
    return "\n".join(parts) + "\n"


def render_all(content_dir: Path = CONTENT) -> dict[Path, str]:
    mappings = load_mappings(content_dir)
    return {
        Path("matrix.md"): matrix_markdown(mappings),
        Path("index.html"): matrix_html(mappings),
        Path("glossary.json"): json.dumps(cards(mappings), indent=2, ensure_ascii=False) + "\n",
    }


def write_all(root: Path = ROOT) -> list[Path]:
    written = []
    for relative, value in render_all().items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        _ = target.write_text(value, encoding="utf-8")
        written.append(target)
    return written


app = typer.Typer(help="Build provider mapping matrices and cards.")


@app.command()
def build(check: bool = typer.Option(False, "--check", help="Fail when a checked-in output differs.")) -> None:
    """Regenerate provider mappings from committed YAML."""
    outputs = render_all()
    if check:
        stale = [
            path.as_posix()
            for path, value in outputs.items()
            if not (ROOT / path).exists() or (ROOT / path).read_text(encoding="utf-8") != value
        ]
        if stale:
            typer.echo(f"Stale provider outputs: {', '.join(stale)}", err=True)
            raise typer.Exit(1)
        typer.echo(f"Provider outputs current ({len(outputs)} files).")
        return
    for path in write_all():
        typer.echo(f"wrote {path.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    app()
