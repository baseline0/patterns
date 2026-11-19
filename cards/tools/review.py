"""Timed terminal review of the canonical card deck.

The browser page in cards/index.html is the visual review path; this CLI is the keyboard-only path. Both use the same
deck.json. Spaced-repetition state is local, unversioned, and written only at the end of a session; --dry-run previews
the session without touching it.
"""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import typer

ROOT = Path(__file__).resolve().parent.parent
DECK = ROOT / "deck.json"
STATE = ROOT / ".review-state.json"
INTERVALS = (1, 3, 7, 14, 30)

app = typer.Typer(help="Timed terminal review of the unified card deck.")


def now_utc() -> datetime:
    return datetime.now(UTC)


def is_due(record: dict[str, Any] | None, now: datetime) -> bool:
    """A card is due when it has never been seen or its due date has passed."""
    if not record or not record.get("due"):
        return True
    try:
        return datetime.fromisoformat(str(record["due"])) <= now
    except ValueError:
        return True


def schedule(record: dict[str, Any] | None, again: bool, now: datetime) -> dict[str, Any]:
    """Advance the box on Good, reset it on Again; due dates are UTC ISO strings."""
    updated = dict(record or {})
    updated["seen"] = int(updated.get("seen", 0)) + 1
    box = int(updated.get("box", 0))
    updated["box"] = 0 if again else min(box + 1, len(INTERVALS) - 1)
    days = 0 if again else INTERVALS[updated["box"]]
    updated["due"] = (now + timedelta(days=days)).isoformat()
    return updated


def select_cards(
    cards: list[dict[str, Any]],
    state: dict[str, Any],
    tag: str | None = None,
    due_only: bool = True,
    shuffle: bool = True,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    """Filter by tag and due date; shuffle with a caller-supplied random module in tests."""
    moment = now or now_utc()
    selected = [
        card
        for card in cards
        if (not tag or tag in card["metadata"]["tags"]) and (not due_only or is_due(state.get(card["id"]), moment))
    ]
    if shuffle:
        random.shuffle(selected)
    return selected


def load_deck() -> list[dict[str, Any]]:
    if not DECK.exists():
        typer.echo(f"Deck not found: {DECK}. Run: uv run python cards/tools/build.py", err=True)
        raise typer.Exit(1)
    payload = json.loads(DECK.read_text(encoding="utf-8"))
    return list(payload.get("cards", []))


def load_state() -> dict[str, Any]:
    return dict(json.loads(STATE.read_text(encoding="utf-8"))) if STATE.exists() else {}


@app.command()
def review(
    tag: str | None = typer.Option(None, "--tag", help="Only cards carrying this tag."),
    minutes: int = typer.Option(30, "--minutes", min=1, help="Session length in minutes."),
    no_shuffle: bool = typer.Option(False, "--no-shuffle", help="Keep deck order."),
    all_cards: bool = typer.Option(False, "--all", help="Include cards that are not due."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview the session; do not write review state."),
) -> None:
    """Review due cards until the timer expires or the queue is empty."""
    cards = load_deck()
    state = load_state()
    queue = select_cards(cards, state, tag=tag, due_only=not all_cards, shuffle=not no_shuffle)
    if dry_run:
        typer.echo(f"{len(queue)} card(s) selected from {len(cards)}; state unchanged ({STATE.name}).")
        for card in queue[:5]:
            typer.echo(f"  - {card['title']}")
        return
    if not queue:
        typer.echo("No cards match. Try --all or a different --tag.")
        return

    started = now_utc()
    deadline = started + timedelta(minutes=minutes)
    reviewed = 0
    for card in queue:
        if now_utc() >= deadline:
            break
        typer.echo(f"\n[{card['metadata']['source']}] {card['title']}")
        input("Reveal [Enter]: ")
        typer.echo(card["body"])
        answer = input("Again (1) / Good (2) [2]: ").strip() or "2"
        state[card["id"]] = schedule(state.get(card["id"]), answer == "1", now_utc())
        reviewed += 1

    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    typer.echo(f"Reviewed {reviewed} card(s); state saved to {STATE.name}.")


if __name__ == "__main__":
    app()
