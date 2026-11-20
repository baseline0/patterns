"""ADR writing practice over committed architecture decision records.

No network or sibling imports; prompts come from docs/adr/*.md and the learner's draft stays on screen only.
"""

from __future__ import annotations

from pathlib import Path

import typer

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ADR_DIR = REPO_ROOT / "docs" / "adr"


def adr_files(directory: Path = ADR_DIR) -> list[Path]:
    files = sorted(directory.glob("*.md"))
    if not files:
        raise ValueError("no ADRs found")
    return files


def title_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


app = typer.Typer(help="Practice writing architecture decision records.")


@app.command()
def list() -> None:
    """List committed ADRs."""
    for path in adr_files():
        typer.echo(f"{path.stem:36} {title_of(path)}")


@app.command()
def drill(adr: str | None = typer.Argument(None, help="ADR filename stem.")) -> None:
    """Prompt for context, options, decision, and consequences, then reveal the committed ADR."""
    files = adr_files()
    if adr:
        files = [path for path in files if path.stem == adr]
        if not files:
            typer.echo(f"Unknown ADR: {adr}", err=True)
            raise typer.Exit(1)
    for path in files:
        typer.echo(f"\nADR: {title_of(path)}")
        typer.echo("Write your own context, options, decision, and consequences before revealing the committed record.")
        typer.prompt("Context in one sentence", default="", show_default=False)
        typer.prompt("Two realistic options", default="", show_default=False)
        typer.prompt("Your decision", default="", show_default=False)
        typer.prompt("One consequence you accept", default="", show_default=False)
        typer.echo("\n--- committed ADR ---")
        typer.echo(path.read_text(encoding="utf-8"))


@app.command()
def prompts() -> None:
    """Print ADR titles as non-interactive writing prompts."""
    for path in adr_files():
        typer.echo(f"Write an ADR for: {title_of(path)}")


if __name__ == "__main__":
    app()
