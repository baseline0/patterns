"""Guards for the unified card module: schema, drift, stable ids, and a content-only boundary."""

from __future__ import annotations

import ast
import importlib.util
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from constants import REPO_ROOT
from typer.testing import CliRunner

ROOT = REPO_ROOT / "cards"
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


build = _load("cards_build", "build.py")
review = _load("cards_review", "review.py")


def test_every_card_matches_the_canonical_schema():
    cards = build.load_cards()
    assert cards
    for card in cards:
        assert set(card) == {"id", "title", "body", "metadata"}
        assert len(card["id"]) == 12
        assert card["title"].strip() and card["body"].strip()
        assert set(card["metadata"]) == {"tags", "source"}
        assert card["metadata"]["tags"]
        assert (REPO_ROOT / card["metadata"]["source"]).is_file()


def test_committed_outputs_have_no_drift():
    outputs = build.render_all()
    assert set(outputs) == {Path("deck.json"), Path("anki.csv"), Path("index.html"), Path("sources.json")}
    for relative, text in outputs.items():
        assert (ROOT / relative).read_text(encoding="utf-8") == text, relative


def test_deck_and_inventory_agree():
    cards = build.load_cards()
    deck = json.loads((ROOT / "deck.json").read_text(encoding="utf-8"))
    inventory = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    assert deck["schema_version"] == build.SCHEMA_VERSION == inventory["schema_version"]
    assert deck["cards"] == cards
    assert inventory["total"] == len(cards)
    assert sum(source["cards"] for source in inventory["sources"]) == len(cards)


def test_ids_are_stable_for_a_source_and_change_with_content(tmp_path):
    glossary = tmp_path / "unit" / "glossary.json"
    glossary.parent.mkdir()
    glossary.write_text('[{"title": "A", "body": "B", "metadata": {"tags": ["t"]}}]', encoding="utf-8")
    first = build.load_cards(tmp_path)[0]["id"]
    assert build.load_cards(tmp_path)[0]["id"] == first
    glossary.write_text('[{"title": "C", "body": "B", "metadata": {"tags": ["t"]}}]', encoding="utf-8")
    assert build.load_cards(tmp_path)[0]["id"] != first


def test_invalid_glossary_is_rejected(tmp_path):
    glossary = tmp_path / "glossary.json"
    glossary.write_text('[{"title": "A", "body": "", "metadata": {"tags": ["t"]}}]', encoding="utf-8")
    with pytest.raises(build.ContentError, match="body"):
        build.load_cards(tmp_path)


def test_anki_csv_has_a_header_and_quotes_multiline_bodies():
    cards = [
        {
            "id": "1",
            "title": "Front",
            "body": "line one\nline two",
            "metadata": {"tags": ["a", "b"], "source": "x/glossary.json"},
        }
    ]
    assert build.anki_csv(cards) == 'Front,Back,Tags\nFront,"line one\nline two",a b\n'


def test_review_page_embeds_the_deck_without_breakout():
    cards = [
        {
            "id": "x",
            "title": "</script><script>alert(1)</script>",
            "body": "body",
            "metadata": {"tags": ["t"], "source": "x/glossary.json"},
        }
    ]
    html = build.review_page(cards)
    assert "fetch(" not in html and "https://" not in html and "cdn" not in html
    assert html.count("<script") == 2
    assert "\\u003c/script\\u003e" in html


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def test_tools_do_not_import_acquisition_or_retrieval_packages():
    for path in sorted(TOOLS.glob("*.py")):
        assert not _imports(path) & BANNED, path.name


def test_schedule_advances_boxes_after_good_and_resets_on_again():
    now = datetime(2026, 1, 1, tzinfo=UTC)
    first = review.schedule(None, False, now)
    assert first["box"] == 1 and first["seen"] == 1
    assert first["due"] == (now + timedelta(days=3)).isoformat()
    second = review.schedule(first, False, now)
    assert second["box"] == 2 and second["due"] == (now + timedelta(days=7)).isoformat()
    reset = review.schedule(second, True, now)
    assert reset["box"] == 0 and reset["due"] == now.isoformat() and reset["seen"] == 3


def test_due_check_and_tag_filter():
    now = datetime(2026, 1, 1, tzinfo=UTC)
    cards = [
        {"id": "a", "title": "A", "metadata": {"tags": ["t"], "source": "g"}},
        {"id": "b", "title": "B", "metadata": {"tags": ["other"], "source": "g"}},
    ]
    future = {"b": {"due": (now + timedelta(days=1)).isoformat()}}
    assert review.is_due(None, now) is True
    assert review.is_due(future["b"], now) is False
    assert [card["id"] for card in review.select_cards(cards, future, now=now, shuffle=False)] == ["a"]
    assert review.select_cards(cards, {}, tag="other", due_only=False, shuffle=False)[0]["id"] == "b"


def test_dry_run_does_not_write_review_state(tmp_path, monkeypatch):
    monkeypatch.setattr(review, "STATE", tmp_path / "state.json")
    result = CliRunner().invoke(review.app, ["--dry-run", "--tag", "claim", "--minutes", "5"])
    assert result.exit_code == 0, result.output
    assert "state unchanged" in result.output
    assert not (tmp_path / "state.json").exists()
