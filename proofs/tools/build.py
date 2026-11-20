"""Render committed proof DAGs into readable notes and review cards.

The YAML in content/ is the source of truth: a statement, an invariant, a dependency DAG of steps, and a complexity
bound. This builder only writes deterministic text under proofs/<id>/; cards/deck.json picks up the generated glossaries.
No network, no sibling imports.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
REQUIRED = ("id", "title", "statement", "invariant", "steps", "complexity")


class ProofError(ValueError):
    """A proof file is missing a required part or has an inconsistent step graph."""


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def load_proofs(content_dir: Path = CONTENT) -> list[dict[str, Any]]:
    proofs = []
    for path in sorted(content_dir.glob("*.yaml")):
        proof = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(proof, dict):
            raise ProofError(f"{path.name}: expected a YAML mapping")
        validate(proof, source=path.name)
        proofs.append(proof)
    if not proofs:
        raise ProofError(f"no proof files in {content_dir}")
    return proofs


def validate(proof: dict[str, Any], source: str) -> None:
    missing = [key for key in REQUIRED if key not in proof]
    if missing:
        raise ProofError(f"{source}: missing {', '.join(missing)}")
    steps = proof["steps"]
    if not isinstance(steps, list) or len(steps) < 2:
        raise ProofError(f"{source}: steps must be a list of at least two steps")
    ids: list[str] = []
    for index, step in enumerate(steps):
        if not isinstance(step, dict) or not text(step.get("id")) or not text(step.get("detail")):
            raise ProofError(f"{source}: step {index} needs an id and detail")
        ids.append(text(step["id"]))
    if len(ids) != len(set(ids)):
        raise ProofError(f"{source}: step ids must be unique")
    known = set(ids)
    for step in steps:
        for dep in step.get("depends_on", []):
            if dep not in known:
                raise ProofError(f"{source}: {step['id']} depends on unknown step {dep!r}")
            if dep == step["id"]:
                raise ProofError(f"{source}: {step['id']} cannot depend on itself")


def cards_for(proof: dict[str, Any], source: str) -> list[dict[str, Any]]:
    proof_id = text(proof["id"])
    family = text(proof.get("family")) or "proof"
    tags = [family, "proof", proof_id]
    entries = [
        {
            "title": f"Prove: {text(proof['title'])}",
            "body": f"{text(proof['statement'])}\n\nComplexity: {text(proof['complexity'])}",
            "metadata": {"tags": [*tags, "statement"], "source": source},
        },
        {
            "title": f"Invariant: {text(proof['title'])}",
            "body": text(proof["invariant"]),
            "metadata": {"tags": [*tags, "invariant"], "source": source},
        },
    ]
    for step in proof["steps"]:
        deps = step.get("depends_on", [])
        body = text(step["detail"])
        if deps:
            body += f"\n\nDepends on: {', '.join(str(dep) for dep in deps)}"
        entries.append(
            {
                "title": f"Proof step: {text(step.get('label')) or text(step['id'])}",
                "body": body,
                "metadata": {"tags": [*tags, "step"], "source": source},
            }
        )
    return entries


def readme(proof: dict[str, Any]) -> str:
    lines = [
        f"# {text(proof['title'])}",
        "",
        "> Generated from `content/`. Edit the YAML, then run `tools/build.py`.",
        "",
        f"**Statement**: {text(proof['statement'])}",
        "",
        f"**Invariant**: {text(proof['invariant'])}",
        "",
        "## Steps",
        "",
    ]
    for step in proof["steps"]:
        deps = step.get("depends_on", [])
        suffix = f" (depends on {', '.join(str(dep) for dep in deps)})" if deps else ""
        lines += [f"- **{text(step.get('label')) or text(step['id'])}**{suffix}: {text(step['detail'])}"]
    lines += ["", f"**Complexity**: {text(proof['complexity'])}"]
    claim_ids = proof.get("claim_ids", [])
    if claim_ids:
        lines += ["", "## Linked claims", ""] + [f"- `{claim}`" for claim in claim_ids]
    return "\n".join(lines).rstrip("\n") + "\n"


def render_all(content_dir: Path = CONTENT) -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    for proof in load_proofs(content_dir):
        proof_id = text(proof["id"])
        source = f"proofs/content/{proof_id}.yaml"
        outputs[Path(f"{proof_id}/README.md")] = readme(proof)
        outputs[Path(f"{proof_id}/glossary.json")] = (
            json.dumps(cards_for(proof, source), indent=2, ensure_ascii=False) + "\n"
        )
    return outputs


def write_all(root: Path = ROOT) -> list[Path]:
    written = []
    for relative, value in render_all().items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        _ = target.write_text(value, encoding="utf-8")
        written.append(target)
    return written


app = typer.Typer(help="Render committed proof DAGs into notes and cards.")


@app.command()
def build(check: bool = typer.Option(False, "--check", help="Fail when a checked-in output differs.")) -> None:
    """Regenerate proof notes and glossaries from the committed DAG YAML."""
    outputs = render_all()
    if check:
        stale = [
            path.as_posix()
            for path, value in outputs.items()
            if not (ROOT / path).exists() or (ROOT / path).read_text(encoding="utf-8") != value
        ]
        if stale:
            typer.echo(f"Stale proof outputs (run the builder): {', '.join(stale)}", err=True)
            raise typer.Exit(1)
        typer.echo(f"Proof outputs current ({len(outputs)} files).")
        return
    for path in write_all():
        typer.echo(f"wrote {path.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    app()
