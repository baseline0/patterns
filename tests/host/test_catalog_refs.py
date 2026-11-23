"""Host-tier contract test: catalog_refs must resolve against the sibling catalog checkout.

This is deliberately not a unit test: it reads a sibling repository, which the unit tier forbids.
Run it locally with the catalog checkout beside this one (the fleet workspace layout does this).
"""

from __future__ import annotations

import json
import re
from typing import Any

import pytest
import yaml
from constants import REPO_ROOT

CATALOG = REPO_ROOT.parent / "catalog"
INDEX = CATALOG / "subjects.json"
CONTENT_FAMILIES = (
    "architecture/content",
    "data-structures/content",
    "design-patterns/content",
    "papers/content",
    "proofs/content",
    "providers/content",
    "testing/content",
)


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


def _subject_index() -> dict[str, str | None]:
    document = json.loads(INDEX.read_text(encoding="utf-8"))
    assert document.get("schema_version") == 1, "unsupported catalog subject index schema"
    subjects = document.get("subjects", {})
    assert subjects, "no subjects in catalog/subjects.json"
    return {subject: entry.get("ontology") for subject, entry in subjects.items()}


def _entity_ids(ontology: str) -> set[str]:
    document = yaml.safe_load((CATALOG / ontology).read_text(encoding="utf-8")) or {}
    return {_normalize(item["name"]) for item in document.get("entity_types", [])}


def test_catalog_refs_resolve_against_the_sibling_catalog() -> None:
    if not INDEX.is_file():
        pytest.skip(f"sibling catalog subject index not found at {INDEX}")

    subjects = _subject_index()
    refs = [
        ref
        for family in CONTENT_FAMILIES
        for path in sorted((REPO_ROOT / family).rglob("*.yaml"))
        for ref in _refs(yaml.safe_load(path.read_text(encoding="utf-8")))
    ]
    assert refs, "no catalog_refs in committed content; the contract has no live example"

    entity_cache: dict[str, set[str]] = {}
    broken: list[str] = []
    for ref in refs:
        if not isinstance(ref, str) or not ref:
            broken.append(f"{ref!r}: expected a shallow subject or subject/id string")
            continue
        subject, separator, entity = ref.partition("/")
        if subject not in subjects:
            broken.append(f"{ref!r}: unknown subject (not in catalog/subjects.json)")
            continue
        if not separator:
            continue
        ontology = subjects[subject]
        if not ontology:
            broken.append(
                f"{ref!r}: subject {subject!r} has no ontology; use a subject-only ref or add one to catalog/subjects.json"
            )
            continue
        if ontology not in entity_cache:
            entity_cache[ontology] = _entity_ids(ontology)
        known = entity_cache[ontology]
        if not known:
            broken.append(f"{ref!r}: ontology {ontology} declares no entity_types")
        elif _normalize(entity) not in known:
            broken.append(f"{ref!r}: unknown entity in {ontology}")

    assert not broken, f"unresolved catalog_refs: {broken}"
