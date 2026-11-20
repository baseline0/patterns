"""Guards for deterministic design, architecture, provider, and drill modules."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

from constants import REPO_ROOT
from typer.testing import CliRunner

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
MODULES = {
    "design": REPO_ROOT / "design-patterns" / "tools" / "build.py",
    "architecture": REPO_ROOT / "architecture" / "tools" / "build.py",
    "quality": REPO_ROOT / "quality" / "tools" / "atam.py",
    "decisions": REPO_ROOT / "decisions" / "tools" / "adr_coach.py",
    "scenarios": REPO_ROOT / "scenarios" / "tools" / "drill.py",
    "providers": REPO_ROOT / "providers" / "tools" / "build.py",
}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


design = _load("design_patterns_build", MODULES["design"])
architecture = _load("architecture_build", MODULES["architecture"])
quality = _load("quality_atam", MODULES["quality"])
decisions = _load("decisions_adr_coach", MODULES["decisions"])
scenarios = _load("scenarios_drill", MODULES["scenarios"])
providers = _load("providers_build", MODULES["providers"])


def test_generated_outputs_have_no_drift():
    roots = {
        "design": REPO_ROOT / "design-patterns",
        "architecture": REPO_ROOT / "architecture",
        "providers": REPO_ROOT / "providers",
    }
    builders = {"design": design, "architecture": architecture, "providers": providers}
    for name, root in roots.items():
        outputs = builders[name].render_all()
        assert outputs
        for relative, text in outputs.items():
            assert (root / relative).read_text(encoding="utf-8") == text, f"{name}/{relative}"


def test_design_patterns_cover_all_categories_and_link_to_catalogue():
    patterns = design.load_patterns()
    assert len(patterns) == 24
    assert {pattern["category"] for pattern in patterns} == {"creational", "structural", "behavioral", "application"}
    assert all(len(pattern["participants"]) >= 2 for pattern in patterns)
    assert all(len(pattern["quiz"]) == 2 for pattern in patterns)


def test_architecture_references_resolve():
    catalogue = architecture.load_catalogue()
    items = architecture.load_all()
    architecture.validate_references(catalogue, items)
    assert {kind: len(group) for kind, group in items.items()} == {
        "styles": 6,
        "tactics": 9,
        "quality-attributes": 6,
    }


def test_catalogue_scenarios_have_all_review_artifacts():
    for scenario in architecture.load_catalogue()["scenarios"]:
        for key in ("path", "hints", "solution", "rubric"):
            assert (REPO_ROOT / scenario[key]).is_file(), f"{scenario['id']}:{key}"


def test_provider_mappings_cover_three_providers_and_fixtures():
    mappings = providers.load_mappings()
    assert len(mappings) == 2
    for mapping in mappings:
        assert set(mapping["providers"]) == {"aws", "azure", "gcp"}
        for provider in mapping["providers"].values():
            assert (REPO_ROOT / provider["plan_fixture"]).is_dir()


def test_drills_are_offline_and_read_committed_content():
    runner = CliRunner()
    quality_result = runner.invoke(quality.app, ["prompts"])
    assert quality_result.exit_code == 0, quality_result.output
    assert "availability" in quality_result.output
    adr_result = runner.invoke(decisions.app, ["list"])
    assert adr_result.exit_code == 0, adr_result.output
    assert "0004-local-system-design-drills" in adr_result.output
    scenario_result = runner.invoke(scenarios.app, ["list"])
    assert scenario_result.exit_code == 0, scenario_result.output
    assert "10-disaster-recovery" in scenario_result.output


def test_scenario_dry_run_does_not_write_state(tmp_path, monkeypatch):
    monkeypatch.setattr(scenarios, "STATE", tmp_path / "state.json")
    result = CliRunner().invoke(
        scenarios.app,
        ["drill", "06-cicd-pipeline", "--minutes", "1", "--dry-run"],
        input="draft notes\n",
    )
    assert result.exit_code == 0, result.output
    assert "rubric" in result.output.lower()
    assert not (tmp_path / "state.json").exists()


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def test_new_tools_do_not_import_acquisition_or_retrieval_packages():
    for path in MODULES.values():
        assert not _imports(path) & BANNED, path.name
