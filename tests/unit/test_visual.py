"""Guards for the visual module: deterministic drift, graph validity, and no external assets."""

from __future__ import annotations

import ast
import importlib.util
import json
import re

import pytest
import yaml
from constants import REPO_ROOT

ROOT = REPO_ROOT / "visual"
TOOLS = ROOT / "tools"
BANNED = {
    "httpx",
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


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = _load("visual_build", "build.py")


def test_committed_visual_outputs_have_no_drift():
    outputs = build.render_all()
    for relative, text in outputs.items():
        assert (ROOT / relative).read_text(encoding="utf-8") == text, relative


def test_inventory_matches_committed_content():
    inventory = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    papers = sorted(path.stem.removeprefix("arxiv-") for path in (REPO_ROOT / "papers/content").glob("*.yaml"))
    patterns = json.loads((REPO_ROOT / "data/patterns.json").read_text(encoding="utf-8"))["patterns"]
    architecture_graph = json.loads((REPO_ROOT / "architecture/graph.json").read_text(encoding="utf-8"))
    assert inventory["papers"] == papers
    assert inventory["patterns"] == [pattern["id"] for pattern in patterns]
    assert inventory["proofs"] == sorted(path.stem for path in (REPO_ROOT / "proofs/content").glob("*.yaml"))
    assert inventory["architecture_nodes"] == [node["id"] for node in architecture_graph.get("nodes", [])]


def test_concept_graph_resolves_related_ids_only():
    paper = {
        "concepts": [
            {"id": "a", "name": "A", "definition": "first", "related": ["b", "missing", "a"]},
            {"id": "b", "name": "B", "definition": "second"},
        ]
    }
    graph = build.concept_graph(paper)
    assert [node["id"] for node in graph["nodes"]] == ["a", "b"]
    assert graph["links"] == [{"source": "a", "target": "b"}]


def test_concept_svg_is_deterministic_and_escapes_labels():
    graph = {
        "nodes": [{"id": "a", "label": "<script>", "definition": "d", "mentions": 0, "related": []}],
        "links": [],
    }
    assert build.concept_svg(graph) == build.concept_svg(graph)
    assert "&lt;script&gt;" in build.concept_svg(graph)
    assert "<script>" not in build.concept_svg(graph)


def test_proof_depths_reject_unknown_and_cyclic_dependencies():
    good = {
        "id": "p",
        "steps": [
            {"id": "a", "label": "A"},
            {"id": "b", "label": "B", "depends_on": ["a"]},
            {"id": "c", "label": "C", "depends_on": ["b"]},
        ],
    }
    assert build.proof_depths(good) == {"a": 0, "b": 1, "c": 2}
    with pytest.raises(build.ContentError, match="unknown"):
        build.proof_depths({"id": "p", "steps": [{"id": "a", "depends_on": ["z"]}]})
    with pytest.raises(build.ContentError, match="cycle"):
        build.proof_depths(
            {
                "id": "p",
                "steps": [
                    {"id": "a", "depends_on": ["b"]},
                    {"id": "b", "depends_on": ["a"]},
                ],
            }
        )


def test_proof_svg_has_one_node_per_step():
    proof = {
        "id": "p",
        "title": "P",
        "steps": [
            {"id": "a", "label": "Base", "detail": "d1"},
            {"id": "b", "label": "Step", "detail": "d2", "depends_on": ["a"]},
        ],
    }
    svg = build.proof_svg(proof)
    assert svg.count("<rect") == 2 and svg.count("<line") == 1
    page = build.proof_page("p", proof)
    assert "Base" in page and "d2" in page


def test_every_generated_page_is_self_contained():
    for path in sorted(ROOT.rglob("*.html")):
        body = path.read_text(encoding="utf-8")
        assert "http://" not in body and "https://" not in body, path
        assert "fetch(" not in body and "cdn" not in body, path


def test_every_relative_link_and_image_resolves():
    for path in sorted(ROOT.rglob("*.html")):
        body = path.read_text(encoding="utf-8")
        links = re.findall(r'(?:href|src)="([^"#]+)"', body)
        for link in links:
            if link.startswith(("http:", "https:", "data:")):
                continue
            assert (path.parent / link).resolve().exists(), f"{path.relative_to(ROOT)}: {link}"


def test_tools_do_not_import_acquisition_or_retrieval_packages():
    for path in sorted(TOOLS.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert not imported & BANNED, path.name


def test_paper_yaml_is_read_without_mutating_it():
    payload = yaml.safe_load((REPO_ROOT / "papers/content/arxiv-2401.12345.yaml").read_text(encoding="utf-8"))
    assert build.concept_graph(payload)["nodes"] == []
    assert payload["concepts"] == []
