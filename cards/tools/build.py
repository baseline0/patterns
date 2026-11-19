"""Build one canonical deck from every committed glossary.json in this repository.

Each family already renders its source YAML into a glossary.json in the patterns unified card format:
{title, body, metadata: {tags}}. This builder is the single consumer of those files. It assigns stable ids, emits a
versioned deck, an Anki CSV, and a self-contained local review page. It reads no network, PDF, or sibling-repo data.

Run `uv run python cards/tools/build.py` to regenerate, or `--check` in tests and CI to detect drift.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path

import typer

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent
SCHEMA_VERSION = 1
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", "cards", "visual"}

REVIEW_PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Patterns card review</title>
<style>
:root{color-scheme:light dark}
body{font-family:system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem;line-height:1.5}
h1{margin-bottom:.25rem}
#controls{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:1rem 0}
.card{border:1px solid #8888;border-radius:12px;padding:1.5rem;min-height:11rem;cursor:pointer}
.front{font-size:1.35rem;font-weight:600}
.back{margin-top:1rem;white-space:pre-wrap}
.back[hidden],#actions[hidden]{display:none}
button,select,input{font:inherit}
button{margin-right:.4rem;padding:.35rem .7rem;border-radius:.5rem;cursor:pointer}
.meta{color:#888;font-size:.85rem}
.progress{height:.5rem;background:#8883;border-radius:1rem;overflow:hidden;margin-bottom:1rem}
.progress span{display:block;height:100%;width:0;background:#3a7;transition:width .2s}
</style>
</head>
<body>
<h1>Card review</h1>
<p class="meta">One deck from every committed glossary.json. Progress is stored in this browser only.</p>
<div id="controls">
<label>Tag <select id="tag"><option value="">All</option></select></label>
<label><input type="checkbox" id="due" checked> Due only</label>
<label><input type="checkbox" id="shuffle" checked> Shuffle</label>
<button id="start">Start 30 min</button>
<span id="timer" class="meta"></span>
</div>
<p class="meta" id="status"></p>
<div class="progress"><span id="bar"></span></div>
<div class="card" id="card"><div class="front" id="front"></div><div class="back" id="back" hidden></div></div>
<div id="actions" hidden><button id="again">Again (1)</button><button id="good">Good (2)</button></div>
<script type="application/json" id="deck">__DECK_JSON__</script>
<script>
(() => {
  const deck = JSON.parse(document.getElementById('deck').textContent);
  const cards = deck.cards;
  const stateKey = 'patterns.cards.v1';
  const state = JSON.parse(localStorage.getItem(stateKey) || '{}');
  const intervals = [1, 3, 7, 14, 30];
  const day = 86400000;
  const el = (id) => document.getElementById(id);
  const tag = el('tag'), dueOnly = el('due'), shuffle = el('shuffle');
  const front = el('front'), back = el('back'), actions = el('actions');
  const status = el('status'), timer = el('timer'), bar = el('bar');
  let queue = [], position = 0, revealed = false, seconds = 1800, ticker = null;

  [...new Set(cards.flatMap(card => card.metadata.tags))].sort().forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    tag.appendChild(option);
  });

  const isDue = (card) => {
    const record = state[card.id];
    return !record || !record.due || Date.parse(record.due) <= Date.now();
  };

  const grade = (again) => {
    const card = queue[position];
    if (!card) return;
    const record = state[card.id] || {box: 0, seen: 0};
    record.seen += 1;
    record.box = again ? 0 : Math.min(record.box + 1, intervals.length - 1);
    record.due = new Date(Date.now() + (again ? 0 : intervals[record.box] * day)).toISOString();
    state[card.id] = record;
    localStorage.setItem(stateKey, JSON.stringify(state));
    position += 1;
    show();
  };

  const show = () => {
    const card = queue[position];
    back.hidden = true;
    actions.hidden = true;
    if (!card) {
      front.textContent = queue.length ? 'Session complete.' : 'No cards match this filter.';
      back.textContent = '';
      status.textContent = queue.length ? `Reviewed ${position} of ${queue.length}.` : 'Adjust the tag or turn off due-only.';
      bar.style.width = queue.length ? '100%' : '0';
      clearInterval(ticker);
      ticker = null;
      return;
    }
    revealed = false;
    front.textContent = card.title;
    back.textContent = card.body;
    status.textContent = `${position + 1} / ${queue.length} · ${card.metadata.tags.join(' · ')} · ${card.metadata.source}`;
    bar.style.width = `${(position / queue.length) * 100}%`;
  };

  const reveal = () => {
    if (!queue[position] || revealed) return;
    revealed = true;
    back.hidden = false;
    actions.hidden = false;
  };

  el('card').addEventListener('click', reveal);
  el('again').addEventListener('click', () => grade(true));
  el('good').addEventListener('click', () => grade(false));
  el('start').addEventListener('click', () => {
    queue = cards.filter(card => (!tag.value || card.metadata.tags.includes(tag.value)) && (!dueOnly.checked || isDue(card)));
    if (shuffle.checked) {
      for (let i = queue.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [queue[i], queue[j]] = [queue[j], queue[i]];
      }
    }
    position = 0;
    seconds = 1800;
    timer.textContent = '30:00';
    clearInterval(ticker);
    ticker = setInterval(() => {
      seconds = Math.max(0, seconds - 1);
      timer.textContent = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
      if (seconds === 0) { clearInterval(ticker); ticker = null; queue = []; show(); }
    }, 1000);
    show();
  });
  document.addEventListener('keydown', event => {
    if (event.code === 'Space') { event.preventDefault(); reveal(); }
    if (event.key === '1' && revealed) grade(true);
    if (event.key === '2' && revealed) grade(false);
  });
  show();
})();
</script>
</body>
</html>
"""


class ContentError(ValueError):
    """A glossary is not in the unified card format."""


def discover_glossaries(root: Path = REPO_ROOT) -> list[Path]:
    """Every committed glossary.json, excluding generated app directories."""
    return sorted(
        path for path in root.rglob("glossary.json") if not SKIP_DIRS.intersection(path.relative_to(root).parts)
    )


def validate_card(card: object, source: str, index: int) -> None:
    """A card needs a front, a back, and at least one tag."""
    where = f"{source}[{index}]"
    if not isinstance(card, dict):
        raise ContentError(f"{where}: expected an object")
    for key in ("title", "body"):
        if not isinstance(card.get(key), str) or not card[key].strip():
            raise ContentError(f"{where}: {key} must be a non-empty string")
    metadata = card.get("metadata")
    tags = metadata.get("tags") if isinstance(metadata, dict) else None
    if not isinstance(tags, list) or not tags or not all(isinstance(tag, str) and tag for tag in tags):
        raise ContentError(f"{where}: metadata.tags must be a non-empty list of strings")


def load_cards(root: Path = REPO_ROOT) -> list[dict]:
    """Canonical cards with stable ids and their source glossary."""
    cards: list[dict] = []
    seen: set[str] = set()
    for path in discover_glossaries(root):
        source = path.relative_to(root).as_posix()
        entries = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(entries, list):
            raise ContentError(f"{source}: glossary must be a JSON array")
        for index, entry in enumerate(entries):
            validate_card(entry, source, index)
            card_id = hashlib.sha256(f"{source}|{index}|{entry['title']}".encode()).hexdigest()[:12]
            if card_id in seen:
                raise ContentError(f"{source}[{index}]: duplicate card id {card_id}")
            seen.add(card_id)
            cards.append(
                {
                    "id": card_id,
                    "title": entry["title"],
                    "body": entry["body"],
                    "metadata": {
                        "tags": list(dict.fromkeys(entry["metadata"]["tags"])),
                        "source": source,
                    },
                }
            )
    if not cards:
        raise ContentError(f"no glossary.json cards found under {root}")
    return cards


def anki_csv(cards: list[dict]) -> str:
    """Anki import: front, back, space-separated tags; import with 'contains field names' enabled."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["Front", "Back", "Tags"])
    for card in cards:
        writer.writerow([card["title"], card["body"], " ".join(card["metadata"]["tags"])])
    return buffer.getvalue()


def review_page(cards: list[dict]) -> str:
    """Self-contained HTML: no fetch, no CDN, no sibling imports; works from file://."""
    deck = json.dumps({"schema_version": SCHEMA_VERSION, "cards": cards}, ensure_ascii=False)
    safe_deck = deck.replace("<", "\\u003c").replace(">", "\\u003e")
    return REVIEW_PAGE.replace("__DECK_JSON__", safe_deck)


def render_all(root: Path = REPO_ROOT) -> dict[Path, str]:
    """Every generated file as text, keyed by its path under cards/. Pure: writes nothing."""
    cards = load_cards(root)
    counts: dict[str, int] = {}
    for card in cards:
        source = card["metadata"]["source"]
        counts[source] = counts.get(source, 0) + 1
    deck = {"schema_version": SCHEMA_VERSION, "cards": cards}
    return {
        Path("deck.json"): json.dumps(deck, indent=2, ensure_ascii=False) + "\n",
        Path("anki.csv"): anki_csv(cards),
        Path("index.html"): review_page(cards),
        Path("sources.json"): json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "total": len(cards),
                "sources": [{"path": source, "cards": count} for source, count in counts.items()],
            },
            indent=2,
        )
        + "\n",
    }


def write_all(root: Path = ROOT) -> list[Path]:
    """Write every generated file under cards/."""
    written = []
    for relative, text in render_all().items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        _ = target.write_text(text, encoding="utf-8")
        written.append(target)
    return written


app = typer.Typer(help="Build the unified card deck from committed glossaries.")


@app.command()
def build(check: bool = typer.Option(False, "--check", help="Fail when a checked-in output differs.")) -> None:
    """Regenerate the deck, the Anki CSV, and the local review page."""
    outputs = render_all()
    if check:
        stale = [
            relative.as_posix()
            for relative, text in outputs.items()
            if not (ROOT / relative).exists() or (ROOT / relative).read_text(encoding="utf-8") != text
        ]
        if stale:
            typer.echo(f"Stale card outputs (run the builder): {', '.join(stale)}", err=True)
            raise typer.Exit(1)
        typer.echo(f"Card outputs current ({len(outputs)} files).")
        return
    for path in write_all():
        typer.echo(f"wrote {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    app()
