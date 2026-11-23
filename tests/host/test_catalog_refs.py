"""Host-tier contract test: catalog_refs must resolve against the sibling catalog checkout.

This is deliberately not a unit test: it reads a sibling repository, which the unit tier forbids.
Run it locally with the catalog checkout beside this one (the fleet workspace layout does this).
"""

from __future__ import annotations

import re
from typing import Any

import pytest
import yaml
from constants import REPO_ROOT

CATALOG = REPO_ROOT.parent / "catalog"
CONTENT_FAMILIES = (
    "architecture/content",
    "data-structures/content",
    "design-patterns/content",
    "papers/content",
    "proofs/content",
    "providers/content",
    "testing/content",
)
SUBJECT_LINE = re.compile(r"^- ([a-z0-9]+(?:-[a-z0-9]+)*):")


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _refs(node: Any) -> list[Any]:
    if isinstance(node, dict):
        value = node.get("catalog_refs", [])
        found = value if isinstance(value, list) else [value]
        for child in node.values():
            found.extend(_refs(child))
        return found
    if isinstance(node, list):
        return [ref for child in node for ref in _refs(child)]
    return []


def _subject_ids() -> set[str]:
    readme = (CATALOG / "README.md").read_text(encoding="utf-8")
    section = readme.split("## Subjects", 1)[1].split("\n## ", 1)[0]
    return {match.group(1) for line in section.splitlines() if (match := SUBJECT_LINE.match(line))}


def _entity_ids(subject: str) -> set[str]:
    ontology = CATALOG / subject / "ontology.yaml"
    if not ontology.is_file():
        return set()
    document = yaml.safe_load(ontology.read_text(encoding="utf-8")) or {}
    return {_normalize(item["name"]) for item in document.get("entity_types", [])}


def test_catalog_refs_resolve_against_the_sibling_catalog() -> None:
    if not (CATALOG / "README.md").is_file():
        pytest.skip(f"sibling catalog checkout not found at {CATALOG}")

    subjects = _subject_ids()
    assert subjects, "no subjects parsed from catalog/README.md"

    refs = [
        ref
        for family in CONTENT_FAMILIES
        for path in sorted((REPO_ROOT / family).rglob("*.yaml"))
        for ref in _refs(yaml.safe_load(path.read_text(encoding="utf-8")))
    ]
    assert refs, "no catalog_refs in committed content; the contract has no live example"

    broken: list[str] = []
    for ref in refs:
        if not isinstance(ref, str) or "/" not in ref:
            broken.append(f"{ref!r}: expected subject/id")
            continue
        subject, entity = ref.split("/", 1)
        if subject not in subjects:
            broken.append(f"{ref!r}: unknown subject")
        elif _entity_ids(subject) and _normalize(entity) not in _entity_ids(subject):
            broken.append(f"{ref!r}: unknown entity in {subject}/ontology.yaml")

    assert not broken, f"unresolved catalog_refs: {broken}"
