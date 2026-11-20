"""Timed system-design scenario drills with progressive reveal.

Source of truth: architecture/content/catalogue.yaml plus each scenario's README, SOLUTION_HINTS, SOLUTION, and RUBRIC.
Local notes stay in scenarios/.drill-state.json and are gitignored.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
import yaml

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent
CATALOGUE = REPO_ROOT / "architecture" / "content" / "catalogue.yaml"
STATE = ROOT / ".drill-state.json"


def load_scenarios(path: Path = CATALOGUE) -> list[dict[str, Any]]:
    catalogue = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(catalogue, dict) or "scenarios" not in catalogue:
        raise ValueError("catalogue.yaml needs a scenarios list")
    return catalogue["scenarios"]


def scenario_by_id(scenario_id: str) -> dict[str, Any]:
    for scenario in load_scenarios():
        if scenario["id"] == scenario_id:
            return scenario
    raise ValueError(f"unknown scenario: {scenario_id}")


def read(location: str) -> str:
    return (REPO_ROOT / location).read_text(encoding="utf-8")


def record(scenario_id: str, notes: str, dry_run: bool) -> None:
    if dry_run:
        return
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    state[scenario_id] = notes
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


app = typer.Typer(help="Timed system-design drills over committed scenarios.")


@app.command()
def list() -> None:
    """List catalogued scenarios and status."""
    for scenario in load_scenarios():
        typer.echo(f"{scenario['id']:24} {scenario['status']:12} {scenario['title']}")


@app.command()
def drill(
    scenario_id: str = typer.Argument(..., help="Scenario id from the catalogue."),
    minutes: int = typer.Option(30, "--minutes", min=1),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing local state."),
) -> None:
    """Show the prompt, collect notes locally, then reveal hints and the rubric."""
    scenario = scenario_by_id(scenario_id)
    typer.echo(f"Scenario {scenario_id}: {scenario['title']} ({minutes} minutes)")
    typer.echo("\n--- prompt ---")
    typer.echo(read(scenario["path"]))
    notes = typer.prompt("\nYour design notes", default="", show_default=False)
    record(scenario_id, notes, dry_run)
    typer.echo("\n--- hints ---")
    typer.echo(read(scenario["hints"]))
    typer.echo("\n--- rubric ---")
    typer.echo(read(scenario["rubric"]))
    typer.echo(f"\nModel solution: {scenario['solution']}")


@app.command()
def reveal(
    scenario_id: str = typer.Argument(..., help="Scenario id from the catalogue."),
    section: str = typer.Option("solution", "--section", help="solution|hints|rubric"),
) -> None:
    """Print one committed scenario artifact."""
    scenario = scenario_by_id(scenario_id)
    if section not in {"solution", "hints", "rubric"}:
        typer.echo("section must be solution, hints, or rubric", err=True)
        raise typer.Exit(1)
    typer.echo(read(scenario[section]))


if __name__ == "__main__":
    app()
