"""Contract guards for the catalog / patterns boundary.

`catalog` (L3, private) owns domain subject data and provenance. This repo (L2, public) owns reusable pattern
structure, teaching content and rendering. The two are linked by reference, never by import or ingestion.

These live in the unit tier so they run in the same gate as the other design-intent guards.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

import pytest
import yaml
from constants import REPO_ROOT

README = REPO_ROOT / "README.md"
ADR = REPO_ROOT / "docs" / "adr" / "0005-catalog-boundary.md"
MARKER = "<!-- catalog-boundary: subject-data-vs-pattern-rendering -->"

# A catalog_ref is a shallow subject/id reference, never a path into another checkout.
CATALOG_REF = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*$")
CONTENT_FAMILIES = (
    "architecture/content",
    "data-structures/content",
    "design-patterns/content",
    "papers/content",
    "proofs/content",
    "providers/content",
    "testing/content",
)
SKIP_PARTS = {".venv", "node_modules", "__pycache__", "tests"}


def _python_sources() -> list[Path]:
    """Runtime and build Python only: the tests themselves name the forbidden paths on purpose."""
    return [
        path
        for path in REPO_ROOT.rglob("*.py")
        if not any(part in SKIP_PARTS for part in path.parts)
    ]


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    } | {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }


def _refs(node: Any) -> list[Any]:
    """Find every catalog_ref value in a YAML document, at any depth."""
    if isinstance(node, dict):
        value = node.get("catalog_refs", [])
        found = value if isinstance(value, list) else [value]
        for child in node.values():
            found.extend(_refs(child))
        return found
    if isinstance(node, list):
        return [ref for child in node for ref in _refs(child)]
    return []


# --- documentation crumbs ---------------------------------------------------------------------------------------------


def test_readme_declares_the_catalog_boundary() -> None:
    readme = README.read_text(encoding="utf-8")

    assert MARKER in readme
    assert "catalog" in readme and "catalog_refs" in readme
    assert "periodic-table-inspector" in readme


def test_adr_records_the_no_absorption_decision() -> None:
    adr = ADR.read_text(encoding="utf-8")

    assert "# ADR 0005:" in adr
    assert "**Status:** ACCEPTED" in adr
    assert "Option 3" in adr
    assert "catalog_refs" in adr
    assert "periodic-table-inspector" in adr


# --- runtime boundary -------------------------------------------------------------------------------------------------


def test_runtime_python_never_imports_catalog() -> None:
    offenders = [path.relative_to(REPO_ROOT).as_posix() for path in _python_sources() if "catalog" in _imports(path)]

    assert not offenders, f"catalog imported from: {offenders}"


def test_runtime_python_has_no_sibling_catalog_paths() -> None:
    offenders = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in _python_sources()
        if "../catalog" in path.read_text(encoding="utf-8") or "/catalog/" in path.read_text(encoding="utf-8")
    ]

    assert not offenders, f"sibling catalog path in: {offenders}"


# --- reference shape --------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["algorithms", "technology/protocol", "study-designs/cohort"])
def test_catalog_ref_accepts_shallow_ids(value: str) -> None:
    assert CATALOG_REF.fullmatch(value) is not None


@pytest.mark.parametrize(
    "value",
    [
        "/algorithms",
        "../catalog",
        "algorithms/../../secrets",
        "data/drugs.json",
        "https://example.com/algorithms",
    ],
)
def test_catalog_ref_rejects_paths_and_urls(value: str) -> None:
    assert CATALOG_REF.fullmatch(value) is None


def test_committed_catalog_refs_are_shallow_ids() -> None:
    offenders: list[str] = []
    for family in CONTENT_FAMILIES:
        for path in sorted((REPO_ROOT / family).glob("*.yaml")):
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            for ref in _refs(document):
                if not isinstance(ref, str) or CATALOG_REF.fullmatch(ref) is None:
                    offenders.append(f"{path.relative_to(REPO_ROOT).as_posix()}: {ref!r}")

    assert not offenders, f"invalid catalog_refs: {offenders}"
