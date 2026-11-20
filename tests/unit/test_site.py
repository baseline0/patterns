"""Guards for the local site explorer: deterministic drift, catalog integrity, and cross-links."""

from __future__ import annotations

import importlib.util
import json

from constants import REPO_ROOT

ROOT = REPO_ROOT / "site"
TOOLS = ROOT / "tools"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = _load("site_build", "build.py")


def _catalog() -> dict:
    return json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))


def test_committed_site_outputs_have_no_drift():
    outputs = build.render_all()
    for path, value in outputs.items():
        target = path if path.is_absolute() else ROOT / path
        assert target.read_text(encoding="utf-8") == value, target.relative_to(REPO_ROOT)


def test_catalog_items_have_unique_uids_and_existing_targets():
    catalog = _catalog()
    items = catalog["items"]
    assert catalog["total"] == len(items)
    uids = [item["uid"] for item in items]
    assert len(uids) == len(set(uids))
    for item in items:
        source = item.get("source")
        if source:
            assert (REPO_ROOT / source).exists(), f"{item['uid']} missing source {source}"
        for link in item.get("links", []):
            path = str(link.get("path", "")).split("#", 1)[0]
            if not path:
                continue
            assert (REPO_ROOT / path).exists(), f"{item['uid']} missing link {path}"


def test_catalog_surfaces_and_cross_links_present():
    catalog = _catalog()
    by_uid = {item["uid"]: item for item in catalog["items"]}
    assert "site:interactive:site-explorer" in by_uid
    assert "review:interactive:cards-review" in by_uid
    assert "review:interactive:visual-hub" in by_uid
    assert "proofs:reference:lean4-tactics" in by_uid

    proof = next(item for item in catalog["items"] if item["family"] == "proofs" and item["kind"] == "proof")
    labels = [link["label"] for link in proof["links"]]
    assert any(label in {"Proof graph", "Open in explorer"} for label in labels)
    assert any(link["path"].endswith(f"#{proof['uid']}") for link in proof["links"] if link["label"] == "Open in explorer")

    paper = next(item for item in catalog["items"] if item["family"] == "papers")
    assert all(key in paper for key in ("concepts", "claims", "rights"))
    assert any(link["label"] == "Concept map" for link in paper["links"])

    ds = next(item for item in catalog["items"] if item["family"] == "data-structures")
    assert "claims" in ds and "complexity" in ds and "signals" in ds

    arch = next(item for item in catalog["items"] if item["family"] == "architecture" and item["kind"] == "tactic")
    assert "quality_impacts" in arch or "failure_modes" in arch or "tradeoffs" in arch
