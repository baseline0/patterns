"""Read-only MCP server exposing the patterns index to tool-* repos."""

from __future__ import annotations

import json

import typer
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from .index import get_pattern, list_families, list_patterns, search_patterns

READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)


def list_families_tool() -> str:
    return json.dumps(list_families(), ensure_ascii=False)


def list_patterns_tool(family: str = "", kind: str = "") -> str:
    items = list_patterns(family=family or None, kind=kind or None)
    return json.dumps([{"id": i.id, "title": i.title, "family": i.family, "kind": i.kind, "summary": i.summary,
                       "source": i.source, "tags": i.tags} for i in items], ensure_ascii=False)


def search_patterns_tool(query: str) -> str:
    items = search_patterns(query)
    return json.dumps([{"id": i.id, "title": i.title, "family": i.family, "kind": i.kind, "summary": i.summary} for i in items],
                      ensure_ascii=False)


def get_pattern_tool(pattern_id: str) -> str:
    item = get_pattern(pattern_id)
    if item is None:
        return json.dumps({"ok": False, "error": f"unknown pattern: {pattern_id}"})
    return json.dumps({"ok": True, "id": item.id, "title": item.title, "family": item.family, "kind": item.kind,
                       "summary": item.summary, "source": item.source, "tags": item.tags}, ensure_ascii=False)


def build_server() -> MCPServer:
    server = MCPServer("patterns")
    server.add_tool(list_families_tool, name="list_families", description="List pattern families.", annotations=READ_ONLY)
    server.add_tool(list_patterns_tool, name="list_patterns", description="List patterns, optionally filtered by family/kind.", annotations=READ_ONLY)
    server.add_tool(search_patterns_tool, name="search_patterns", description="Search patterns by text.", annotations=READ_ONLY)
    server.add_tool(get_pattern_tool, name="get_pattern", description="Get one pattern's metadata.", annotations=READ_ONLY)
    return server


app = typer.Typer(help="MCP server for patterns index", add_completion=False)


@app.command()
def serve(
    transport: str = typer.Option("stdio", "--transport"),
    host: str = typer.Option("0.0.0.0", "--host"),
    port: int = typer.Option(8080, "--port"),
) -> None:
    if transport == "stdio":
        build_server().run("stdio")
        return
    if transport == "streamable-http":
        from .server import run

        run(host=host, port=port)
        return
    raise typer.BadParameter(f"unsupported transport: {transport}")


if __name__ == "__main__":
    serve()
