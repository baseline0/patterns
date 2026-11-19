#!/usr/bin/env python3
"""Import paper content from a tool-lit-review content export.

This repo is the content and rendering layer. It does not search, download, parse, or index papers. Those steps belong
to tool-lit-review (acquisition and analysis) and tool-rag (indexing and retrieval). The import reads one local JSON
export and writes committed YAML under content/.

Workflow:
1. tool-lit-review fetches a paper and writes fetch_manifest.json
2. tool-lit-review content-export writes the schema-v1 JSON export
3. this command imports the metadata, preserving any concepts, equations, and claims already authored here

The export's schema is owned by tool-lit-review. An unknown schema_version is refused rather than guessed.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import typer
import yaml

app = typer.Typer(help="Import paper content from a tool-lit-review export. No network, no PDF parsing.")
ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SCHEMA_VERSION = 1
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SAFE_ID = re.compile(r"[^A-Za-z0-9._-]+")


class ExportError(ValueError):
    """The export cannot be imported. The message names the problem and the offending paper."""


def _required_string(entry: dict[str, Any], key: str) -> str:
    value = entry.get(key)
    if not isinstance(value, str) or not value:
        raise ExportError(f"paper entry is missing a non-empty {key!r}")
    return value


def _string(entry: dict[str, Any], key: str) -> str | None:
    value = entry.get(key)
    return value if isinstance(value, str) and value else None


def _string_list(entry: dict[str, Any], key: str) -> list[str]:
    value = entry.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _paper_path(paper_id: str, content_dir: Path) -> Path:
    stem = SAFE_ID.sub("_", paper_id.replace("/", ".")).strip("._") or "paper"
    return content_dir / f"arxiv-{stem}.yaml"


def _validate_entry(entry: Any, index: int) -> dict[str, Any]:
    if not isinstance(entry, dict):
        raise ExportError(f"papers[{index}] must be an object")
    paper_id = _required_string(entry, "paper_id")
    pdf = _required_string(entry, "pdf")
    if Path(pdf).is_absolute() or ".." in Path(pdf).parts:
        raise ExportError(f"{paper_id}: pdf must be a path inside the papers folder")
    sha256 = _required_string(entry, "sha256").lower()
    if not SHA256.match(sha256):
        raise ExportError(f"{paper_id}: sha256 must be 64 lowercase hex characters")
    return entry


def load_export(path: Path) -> dict[str, Any]:
    """Read and validate one content export. Unknown fields are ignored; an unknown schema is refused."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ExportError(f"cannot read {path}: {exc}") from exc
    except ValueError as exc:
        raise ExportError(f"{path} is not JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ExportError(f"{path} must hold a JSON object")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ExportError(f"{path}: unsupported schema_version {data.get('schema_version')!r}")
    papers = data.get("papers")
    if not isinstance(papers, list):
        raise ExportError(f"{path}: papers must be a list")
    if not isinstance(data.get("generated_at"), str):
        raise ExportError(f"{path}: generated_at must be an ISO timestamp string")
    data["papers"] = [_validate_entry(entry, index) for index, entry in enumerate(papers)]
    return data


def _read_existing(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        existing = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ExportError(f"{path} is not valid YAML: {exc}") from exc
    if not isinstance(existing, dict):
        raise ExportError(f"{path} must hold a YAML mapping")
    return existing


def _merge(existing: dict[str, Any], entry: dict[str, Any], exported_at: str) -> dict[str, Any]:
    """Update acquisition metadata and keep every authored field. Re-importing is idempotent for authored content."""
    paper_id = _required_string(entry, "paper_id")
    title = _string(entry, "title")
    authors = _string_list(entry, "authors")
    document = dict(existing)
    document["arxiv_id"] = _string(entry, "arxiv_id") or existing.get("arxiv_id") or paper_id
    document.setdefault("version", 1)
    document["date"] = existing.get("date") or exported_at
    current_title = existing.get("title")
    if title and (
        not current_title
        or current_title == paper_id
        or (isinstance(current_title, str) and current_title.startswith("["))
    ):
        document["title"] = title
    document.setdefault("title", paper_id)
    if authors:
        document["authors"] = authors
    document.setdefault("authors", [])
    document.setdefault("abstract", "")
    for key in ("concepts", "equations", "claims", "citations"):
        document.setdefault(key, [])
    document.setdefault("entities", {"people": [], "organizations": []})
    document["source"] = {
        "tool": "tool-lit-review",
        "schema_version": SCHEMA_VERSION,
        "paper_id": paper_id,
        "sha256": _required_string(entry, "sha256").lower(),
        "pdf": _required_string(entry, "pdf"),
        "exported_at": exported_at,
        **{
            key: value
            for key in ("licence", "source", "url", "doi", "published", "categories")
            if (value := entry.get(key)) not in (None, "", [])
        },
    }
    return document


def import_export(export_path: Path, content_dir: Path = CONTENT, *, dry_run: bool = False) -> list[Path]:
    """Import every paper in the export. Returns the YAML paths that were (or would be) written."""
    export = load_export(export_path)
    content_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for entry in export["papers"]:
        target = _paper_path(_required_string(entry, "paper_id"), content_dir)
        document = _merge(_read_existing(target), entry, export["generated_at"])
        written.append(target)
        if not dry_run:
            target.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return written


@app.command("import-export")
def import_export_command(
    export: Path = typer.Option(..., "--export", help="Content export JSON written by tool-lit-review content-export."),
    content: Path = typer.Option(CONTENT, "--content", help="Folder for the committed arxiv-*.yaml files."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print the files that would change; write nothing."),
) -> None:
    """Import tool-lit-review metadata into content/ without touching concepts, equations, or claims."""
    try:
        written = import_export(export, content, dry_run=dry_run)
    except ExportError as error:
        typer.echo(f"import-export: {error}", err=True)
        raise typer.Exit(1) from None
    verb = "would write" if dry_run else "wrote"
    typer.echo(f"{verb} {len(written)} paper file(s) under {content}")
    for path in written:
        typer.echo(f"  {path}")


@app.command("list")
def list_papers() -> None:
    """List all papers in the knowledge base."""
    papers = sorted(CONTENT.glob("arxiv-*.yaml"))
    if not papers:
        typer.echo("No papers imported yet.")
        return
    for paper_file in papers:
        with open(paper_file, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        typer.echo(f"  {data.get('arxiv_id', '?')}: {str(data.get('title', '[No title]'))[:60]}")


if __name__ == "__main__":
    app()
