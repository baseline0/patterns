# Cards

- **Explore in local catalogue:** run `just -f site/justfile serve` and open `site/index.html` (searchable, cross-linked).

One deck for every pattern family. This module is a **consumer** of committed `glossary.json` files; the family builders
(`data-structures/tools/build.py`, `testing/tools/build.py`, `papers/tools/render.py`, `proofs/tools/build.py`) remain the
source of truth.

## Canonical card

A card is the existing patterns unified format plus a stable id and provenance:

```json
{
  "id": "sha256-prefix-of-source-index-title",
  "title": "Claim: sliding-window-avoids-nesting",
  "body": "Sliding window processes each element at most twice...",
  "metadata": {
    "tags": ["arrays-and-2d-arrays", "claim"],
    "source": "data-structures/arrays-and-2d-arrays/glossary.json"
  }
}
```

Rules: `title` and `body` are non-empty strings; `tags` is a non-empty list of strings; `id` and `source` are added by
the builder, never authored by hand. New families join the deck by committing a `glossary.json` in this format.

## Commands

```bash
just -f cards/justfile build          # regenerate deck.json, anki.csv, index.html, sources.json
just -f cards/justfile check          # drift guard: fail if outputs differ from glossaries
just -f cards/justfile preview        # show what a session would review; writes nothing
just -f cards/justfile review --tag trees --minutes 15
just -f cards/justfile serve          # then open http://localhost:8000/cards/index.html
```

`index.html` is self-contained: the deck is embedded, scheduling lives in `localStorage`, and there are no network
requests, CDN scripts, or sibling imports. The terminal review writes `cards/.review-state.json` (gitignored) at the
end of a session; `--dry-run` previews without writing.

## Anki import

Import `anki.csv` with **Fields separated by comma**, **Contains field names** enabled, and tags joined by spaces.
Front = `title`, Back = `body`, Tags = the card's tags.

## Adding cards

1. Edit the family YAML (`data-structures/content/`, `testing/content/`, `papers/content/`, or `proofs/content/`).
2. Run that family's builder to refresh its `glossary.json`.
3. Run `just -f cards/justfile build`, then `uv run pytest tests/unit/test_cards.py`.
