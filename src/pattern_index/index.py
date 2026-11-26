"""Load the committed site/catalog.json index."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .constants import REPO_ROOT
from typing import Any


def _root() -> Path:
    return REPO_ROOT


def catalog_path(root: Path | None = None) -> Path:
    base = root if root is not None else _root()
    return base / "site" / "catalog.json"


def load_catalog(root: Path | None = None) -> dict[str, Any]:
    path = catalog_path(root)
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class PatternItem:
    id: str
    title: str
    family: str
    kind: str
    summary: str
    source: str
    tags: list[str] = field(default_factory=list)


def _to_item(raw: dict[str, Any]) -> PatternItem:
    return PatternItem(
        id=str(raw.get("id", "")),
        title=str(raw.get("title", "")),
        family=str(raw.get("family", "")),
        kind=str(raw.get("kind", "")),
        summary=str(raw.get("summary", "")),
        source=str(raw.get("source", "")),
        tags=list(raw.get("tags") or []),
    )


def list_families(root: Path | None = None) -> list[str]:
    data = load_catalog(root)
    return sorted({i.get("family", "") for i in data.get("items", []) if i.get("family")})


def list_patterns(family: str | None = None, kind: str | None = None, root: Path | None = None) -> list[PatternItem]:
    data = load_catalog(root)
    out = []
    for raw in data.get("items", []):
        if family and raw.get("family") != family:
            continue
        if kind and raw.get("kind") != kind:
            continue
        out.append(_to_item(raw))
    return out


def search_patterns(query: str, root: Path | None = None) -> list[PatternItem]:
    q = query.lower().strip()
    if not q:
        return []
    out = []
    for item in list_patterns(root=root):
        haystack = " ".join([item.id, item.title, item.summary, " ".join(item.tags)]).lower()
        if q in haystack:
            out.append(item)
    return out


def get_pattern(pattern_id: str, root: Path | None = None) -> PatternItem | None:
    for item in list_patterns(root=root):
        if item.id == pattern_id:
            return item
    return None
