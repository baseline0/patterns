"""Boundary guards and tests for the papers content pipeline.

The import is local-only: one JSON export from tool-lit-review, committed YAML here, no download or PDF parsing.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path

import pytest
import yaml
from constants import REPO_ROOT
from typer.testing import CliRunner

PAPERS = REPO_ROOT / "papers"
TOOLS = PAPERS / "tools"
BANNED_ACQUISITION = {
    "httpx",
    "httpx2",
    "requests",
    "urllib",
    "http",
    "aiohttp",
    "pypdf",
    "fitz",
    "arxiv",
    "bs4",
    "feedparser",
    "tool_lit_review",
    "tool_rag",
}


def _load(name: str):
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ingest = _load("ingest")
render = _load("render")


def _export(tmp_path: Path, *, schema_version: int = 1, pdf: str = "pdf/2401.12345.pdf") -> Path:
    path = tmp_path / "papers.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": schema_version,
                "generated_at": "2026-11-10T14:29:02+00:00",
                "papers": [
                    {
                        "paper_id": "2401.12345",
                        "title": "A Paper",
                        "authors": ["Ada Lovelace"],
                        "published": "2024-01-01T00:00:00+00:00",
                        "categories": ["cs.SE"],
                        "doi": None,
                        "arxiv_id": "2401.12345",
                        "licence": "https://creativecommons.org/licenses/by/4.0/",
                        "source": "arxiv",
                        "url": "https://arxiv.org/pdf/2401.12345",
                        "pdf": pdf,
                        "sha256": "a" * 64,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def _paper(tmp_path: Path) -> Path:
    content = tmp_path / "content"
    ingest.import_export(_export(tmp_path), content)
    return content / "arxiv-2401.12345.yaml"


# --- import ----------------------------------------------------------------------------------------------------------


def test_import_writes_metadata_and_the_source_contract(tmp_path: Path) -> None:
    document = yaml.safe_load(_paper(tmp_path).read_text(encoding="utf-8"))

    assert document["arxiv_id"] == "2401.12345"
    assert document["title"] == "A Paper"
    assert document["authors"] == ["Ada Lovelace"]
    assert document["source"]["tool"] == "tool-lit-review"
    assert document["source"]["sha256"] == "a" * 64
    assert document["source"]["pdf"] == "pdf/2401.12345.pdf"
    assert document["concepts"] == []


def test_reimport_preserves_authored_fields(tmp_path: Path) -> None:
    content = tmp_path / "content"
    ingest.import_export(_export(tmp_path), content)
    target = content / "arxiv-2401.12345.yaml"
    document = yaml.safe_load(target.read_text(encoding="utf-8"))
    document["title"] = "An authored title"
    document["concepts"] = [{"id": "c1", "name": "Concept", "definition": "Authored here."}]
    document["claims"] = [{"text": "A claim", "section": "Method"}]
    target.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    ingest.import_export(_export(tmp_path), content)
    after = yaml.safe_load(target.read_text(encoding="utf-8"))

    assert after["title"] == "An authored title"
    assert after["concepts"] == document["concepts"]
    assert after["claims"] == document["claims"]
    assert after["source"]["paper_id"] == "2401.12345"


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    content = tmp_path / "content"

    written = ingest.import_export(_export(tmp_path), content, dry_run=True)

    assert written and not any(path.exists() for path in written)


def test_unknown_schema_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ingest.ExportError, match="schema_version"):
        ingest.import_export(_export(tmp_path, schema_version=2), tmp_path / "content")


def test_pdf_path_outside_the_folder_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ingest.ExportError, match="pdf"):
        ingest.import_export(_export(tmp_path, pdf="../escape.pdf"), tmp_path / "content")


# --- render ----------------------------------------------------------------------------------------------------------


def test_render_outputs_are_derived_from_committed_yaml(tmp_path: Path) -> None:
    paper = yaml.safe_load(_paper(tmp_path).read_text(encoding="utf-8"))
    paper["concepts"] = [{"id": "c1", "name": "Boundary", "definition": "One owner per side.", "mentions": 2}]
    paper["claims"] = [{"text": "Acquisition stays in tool-lit-review.", "section": "Role", "support_level": "design"}]
    paper["equations"] = [{"id": "eq-1", "latex": "a + b", "description": "A sum.", "section": "Intro"}]

    outputs = render.render_outputs(paper, "2401.12345")

    assert set(outputs) == {"README.md", "index.html", "concepts.json", "equations.md", "glossary.json"}
    assert "Boundary" in outputs["README.md"]
    assert json.loads(outputs["concepts.json"])["nodes"][0]["label"] == "Boundary"
    assert "a + b" in outputs["equations.md"]
    assert [entry["metadata"]["tags"] for entry in json.loads(outputs["glossary.json"])] == [
        ["2401.12345", "concept"],
        ["2401.12345", "claim"],
    ]


def test_render_cli_exposes_the_arxiv_argument() -> None:
    result = CliRunner().invoke(render.app, ["--help"])

    assert result.exit_code == 0, result.output
    assert "arxiv" in result.output.lower()


def test_imported_papers_record_original_summary_rights() -> None:
    imported = 0
    for path in sorted((PAPERS / "content").glob("arxiv-*.yaml")):
        paper = yaml.safe_load(path.read_text(encoding="utf-8"))
        source = paper.get("source")
        if not isinstance(source, dict) or not source.get("paper_id"):
            continue
        imported += 1
        assert paper.get("abstract", "").strip(), path.name
        rights = paper.get("rights")
        assert isinstance(rights, dict) and rights.get("quotes") == "none", path.name
        assert rights.get("basis") == "original-summary", path.name
        assert not source.get("licence"), path.name
        assert len(str(source.get("sha256", ""))) == 64, path.name
    assert imported >= 2


def test_committed_paper_outputs_have_no_drift() -> None:
    for path in sorted((PAPERS / "content").glob("arxiv-*.yaml")):
        paper = yaml.safe_load(path.read_text(encoding="utf-8"))
        source = paper.get("source")
        if not isinstance(source, dict) or not source.get("paper_id"):
            continue
        arxiv_id = path.stem.removeprefix("arxiv-")
        target = PAPERS / arxiv_id
        outputs = render.render_outputs(paper, arxiv_id)
        assert set(outputs) == {"README.md", "index.html", "concepts.json", "equations.md", "glossary.json"}
        for name, value in outputs.items():
            assert (target / name).read_text(encoding="utf-8") == value, f"{arxiv_id}/{name}"


# --- identity guards -------------------------------------------------------------------------------------------------


def test_readme_declares_the_content_role_and_neighbours() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    papers_readme = (PAPERS / "README.md").read_text(encoding="utf-8")

    assert "<!-- repo-role: content-and-rendering -->" in readme
    assert "tool-lit-review" in readme and "tool-rag" in readme
    assert "content-export" in papers_readme
    assert "import-export" in papers_readme


def test_papers_tools_import_no_acquisition_or_indexing_code() -> None:
    for path in sorted(TOOLS.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported = {
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        } | {
            alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names
        }
        assert imported.isdisjoint(BANNED_ACQUISITION), f"{path.name} imports acquisition or indexing code"


def test_no_python_in_the_repo_imports_a_sibling_tool() -> None:
    """Content repos consume files and contracts, never sibling modules at runtime."""
    offenders: list[str] = []
    for path in REPO_ROOT.rglob("*.py"):
        if any(part in {".venv", "node_modules", "__pycache__"} for part in path.parts):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        modules = {
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        } | {
            alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names
        }
        if modules & {"tool_lit_review", "tool_rag"}:
            offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert not offenders, f"sibling imports found in: {offenders}"


def test_papers_hold_no_pdf_files() -> None:
    """PDFs belong to the acquisition working folder; this repo commits metadata and authored content only."""
    assert not [path for path in PAPERS.rglob("*.pdf") if ".venv" not in path.parts]
