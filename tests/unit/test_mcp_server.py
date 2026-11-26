"""Smoke tests for the patterns MCP server."""

from __future__ import annotations

import json

from pattern_index.mcp_server import (
    build_server,
    get_pattern_tool,
    list_families_tool,
    list_patterns_tool,
    search_patterns_tool,
)


def test_list_families_tool():
    result = json.loads(list_families_tool())
    assert isinstance(result, list)
    assert "design-patterns" in result


def test_list_patterns_tool():
    result = json.loads(list_patterns_tool(family="design-patterns"))
    assert len(result) > 0
    assert all(r["family"] == "design-patterns" for r in result)


def test_search_patterns_tool():
    result = json.loads(search_patterns_tool("observer"))
    assert isinstance(result, list)


def test_get_pattern_tool_unknown():
    result = json.loads(get_pattern_tool("no-such-pattern-xyz"))
    assert result["ok"] is False


def test_get_pattern_tool_known():
    result = json.loads(list_patterns_tool())
    assert result
    pid = result[0]["id"]
    got = json.loads(get_pattern_tool(pid))
    assert got["ok"] is True
    assert got["id"] == pid


def test_build_server():
    server = build_server()
    assert server is not None
