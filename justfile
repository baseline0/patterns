# Shared commit recipe from fleet-base. Literal path: just does not interpolate variables into import paths.
# Cloud Patterns — local development recipes

# Show available recipes
import 'just/repo-push.just'

import 'just/fleet-clean.just'
import 'just/fleet-checks.just'
import 'just/fleet-commit.just'
import 'just/fleet-test.just'

@help:
    just --list

# === Local Development ===

# Fast iteration: Python HTTP server (local paths, no Docker)
@dev:
    echo "🚀 Starting development server on http://localhost:8000/"
    echo "   (Note: paths are root-relative, not /patterns/)"
    python -m http.server 8000

# Integrated review: Docker Compose (realistic paths, API proxy)
@up:
    echo "🚀 Starting gateway + API on http://localhost:8080/"
    docker compose up gateway api

# Start in background, show URLs
@up-bg:
    docker compose up -d gateway api
    echo "✅ Gateway started"
    echo "   - Patterns: http://localhost:8080/patterns/"
    echo "   - API:      http://localhost:8080/api/"
    echo "   - Health:   http://localhost:8080/healthz"

# Stop services
@down:
    docker compose down

# Health check
@check:
    #!/bin/bash
    echo "🔍 Running health checks..."
    curl -fsS http://localhost:8080/healthz && echo "✓ Gateway healthy" || echo "✗ Gateway down"
    curl -fsS http://localhost:8080/patterns/ > /dev/null && echo "✓ Patterns reachable" || echo "✗ Patterns 404"
    echo "Done."

# === Build & Preview ===

# View logs (for Docker Compose)
@logs:
    docker compose logs -f gateway api

# Restart services
@restart:
    docker compose restart

# Clean up Docker resources
# Renamed from `clean`: tears down Docker resources (compose down -v, system prune); it is not a file clean. The shared clean (fleet-clean.just) removes caches only.
@clean-docker:
    docker compose down -v
    docker system prune -f

# === Testing & Validation ===

# Validate patterns.json schema and assets
@validate:
    python tests/validate_patterns.py

# Run tests
# Unit tests only, matching CI and the pre-push hook. Data validation is `just validate`.
test: test-unit

# Validate + watch for changes
@test-watch:
    #!/bin/bash
    echo "Watching for changes..."
    while true; do
        clear
        python tests/validate_patterns.py || true
        sleep 2
        # Watch for changes in data/ directory
        inotifywait -e modify data/patterns.json assets/diagrams/*.svg 2>/dev/null || sleep 2
    done

# Unit tests only (what CI and the pre-push gate run). Self-contained: depends on no other recipe.
test-unit:
    #!/usr/bin/env bash
    set -euo pipefail
    if uv run pytest --version >/dev/null 2>&1; then
        uv run pytest -m unit --tb=short -v
        exit 0
    fi
    echo "error: test-unit cannot run in this repo: install pytest as a dev dependency (uv add --dev pytest)" >&2
    exit 1

# ============================================================================
# Shared fleet recipes, run by fleet-base's installed tool (run `just -f $FLEET_ROOT/fleet-base/justfile install-fleet`; ADR-020).
# Each line calls `fleet recipe NAME`; define a recipe here instead to override it.
# ============================================================================
