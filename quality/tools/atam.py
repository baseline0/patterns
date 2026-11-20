"""Interactive ATAM-lite drills over committed quality-attribute YAML.

No network or sibling imports; the quality definitions live in architecture/content/quality-attributes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
QUALITY = REPO_ROOT / "architecture" / "content" / "quality-attributes"


def load_attributes(directory: Path = QUALITY) -> list[dict[str, Any]]:
    attributes = []
    for path in sorted(directory.glob("*.yaml")):
        item = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(item, dict) or not all(
            key in item for key in ("id", "name", "stimulus", "response", "measure", "tactics")
        ):
            raise ValueError(f"{path.name}: incomplete quality attribute")
        attributes.append(item)
    if not attributes:
        raise ValueError("no quality attributes found")
    return attributes


app = typer.Typer(help="Practice quality-attribute reasoning with ATAM-lite drills.")


@app.command()
def list() -> None:
    """List quality attributes and their measures."""
    for item in load_attributes():
        typer.echo(f"{item['id']:20} {item['name']:24} {item['measure']}")


@app.command()
def drill(attribute: str | None = typer.Argument(None, help="Quality attribute id.")) -> None:
    """Prompt for response, measure, and tactic, then reveal the committed answer."""
    items = load_attributes()
    if attribute:
        items = [item for item in items if item["id"] == attribute]
        if not items:
            typer.echo(f"Unknown quality attribute: {attribute}", err=True)
            raise typer.Exit(1)
    score = 0
    for item in items:
        typer.echo(f"\nStimulus: {item['stimulus']}")
        typer.echo(f"Target attribute: {item['name']}")
        typer.prompt("What response should the system produce?", default="", show_default=False)
        typer.prompt("What metric would prove it?", default="", show_default=False)
        answer = typer.prompt("Which tactic from the list applies?", default="").strip()
        if answer in item["tactics"]:
            score += 1
            typer.echo("tactic recognized")
        else:
            typer.echo(f"Expected one of: {', '.join(item['tactics'])}")
        typer.echo(f"Committed answer: {item['response']} / {item['measure']}")
    typer.echo(f"\nTactics recognized: {score}/{len(items)}")


@app.command()
def prompts() -> None:
    """Print all quality-attribute stimuli as non-interactive review prompts."""
    for item in load_attributes():
        typer.echo(f"[{item['id']}] {item['stimulus']} -> {item['measure']}")


if __name__ == "__main__":
    app()
