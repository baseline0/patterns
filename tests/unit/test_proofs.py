"""Guards for proof DAGs: schema, claim links, drift, and review-card coverage."""

from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path

import yaml
from constants import REPO_ROOT

ROOT = REPO_ROOT / "proofs"
TOOLS = ROOT / "tools"
BANNED = {"httpx", "requests", "urllib", "http", "aiohttp", "pypdf", "fitz", "tool_lit_review", "tool_rag"}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


proof_build = _load("proof_build", TOOLS / "build.py")
visual_build = _load("proof_visual_build", REPO_ROOT / "visual/tools/build.py")
ds_build = _load("proof_ds_build", REPO_ROOT / "data-structures/tools/build.py")


def test_every_committed_proof_validates():
    proofs = proof_build.load_proofs()
    assert len(proofs) >= 3
    for proof in proofs:
        depths = visual_build.proof_depths(proof)
        assert depths and max(depths.values()) >= 1
        assert proof["invariant"]
        assert proof["complexity"]


def test_claim_links_point_to_real_data_structure_claims():
    known = {claim["id"] for topic in ds_build.load_topics() for claim in topic["claims"]}
    for proof in proof_build.load_proofs():
        assert proof.get("claim_ids"), proof["id"]
        assert set(proof["claim_ids"]) <= known, proof["id"]


def test_committed_proof_outputs_have_no_drift():
    outputs = proof_build.render_all()
    assert outputs
    for relative, value in outputs.items():
        assert (ROOT / relative).read_text(encoding="utf-8") == value, relative


def test_cards_cover_statement_invariant_and_every_step():
    for proof in proof_build.load_proofs():
        source = f"proofs/content/{proof['id']}.yaml"
        cards = proof_build.cards_for(proof, source)
        titles = [card["title"] for card in cards]
        assert titles[0].startswith("Prove:")
        assert titles[1].startswith("Invariant:")
        assert sum(title.startswith("Proof step:") for title in titles) == len(proof["steps"])
        assert all(card["metadata"]["source"] == source for card in cards)
        assert all("proof" in card["metadata"]["tags"] and proof["id"] in card["metadata"]["tags"] for card in cards)


def test_proof_yaml_files_are_unchanged_by_validation():
    path = ROOT / "content" / "heapify-linear.yaml"
    before = path.read_text(encoding="utf-8")
    proof_build.load_proofs()
    assert path.read_text(encoding="utf-8") == before
    assert yaml.safe_load(before)["id"] == "heapify-linear"


def test_proof_tools_do_not_import_acquisition_or_retrieval_packages():
    for path in sorted(TOOLS.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert not imported & BANNED, path.name


def test_generated_glossaries_are_valid_json_arrays():
    for path in sorted(ROOT.glob("*/glossary.json")):
        cards = json.loads(path.read_text(encoding="utf-8"))
        assert cards and all(set(card) == {"title", "body", "metadata"} for card in cards)
