"""Unit tests for the patterns index loader."""

from __future__ import annotations

from pathlib import Path

from constants import REPO_ROOT

from pattern_index.index import get_pattern, list_families, list_patterns, search_patterns

ROOT = REPO_ROOT


def test_list_families_nonempty():
    families = list_families(ROOT)
    assert "design-patterns" in families


def test_list_patterns_design_patterns():
    items = list_patterns(family="design-patterns", root=ROOT)
    assert len(items) > 0
    assert all(i.family == "design-patterns" for i in items)


def test_search_patterns():
    items = search_patterns("observer", root=ROOT)
    assert any("observer" in i.id.lower() or "observer" in i.title.lower() for i in items)


def test_get_pattern_unknown():
    assert get_pattern("no-such-pattern-xyz", root=ROOT) is None


def test_get_pattern_known():
    items = list_patterns(root=ROOT)
    assert items
    found = get_pattern(items[0].id, root=ROOT)
    assert found is not None
    assert found.id == items[0].id
