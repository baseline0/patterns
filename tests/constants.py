"""Repository root for patterns."""

from pathlib import Path

# This repository's root: tests/constants.py -> repo root
REPO_ROOT: Path = Path(__file__).resolve().parents[1]
