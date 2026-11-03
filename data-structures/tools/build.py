"""Generate every output for the data-structures family from the YAML sources in content/.

Outputs (all generated; edit the YAML, then run this file):
    README.md        the topic write-up, complexity table, signals, and problem mapping
    quiz_guide.md    the quiz with answers and explanations
    index.html       a single static page with the same content
    flashcards.csv   Anki-importable cards: one per quiz item and one per complexity row

Run with no arguments to write the outputs. tests/test_data_structures.py regenerates them in memory and fails
when a checked-in file differs, so an output cannot drift from its source.
"""

from __future__ import annotations

import csv
import html
import io
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
REQUIRED_TOPIC_KEYS = ("id", "title", "summary", "mechanics", "claims", "complexity", "signals", "problems", "quiz")


class ContentError(ValueError):
    """A topic file is missing a required part or has an inconsistent value."""


def load_topics(content_dir: Path = CONTENT) -> list[dict]:
    topics = []
    for path in sorted(content_dir.glob("*.yaml")):
        topic = yaml.safe_load(path.read_text(encoding="utf-8"))
        validate(topic, source=path.name)
        topics.append(topic)
    if not topics:
        raise ContentError(f"no topic files found in {content_dir}")
    return topics


def validate(topic: dict, source: str) -> None:
    missing = [key for key in REQUIRED_TOPIC_KEYS if key not in topic]
    if missing:
        raise ContentError(f"{source}: missing {', '.join(missing)}")
    for index, item in enumerate(topic["quiz"]):
        choices = item.get("choices", [])
        if not 0 <= item.get("answer", -1) < len(choices):
            raise ContentError(f"{source}: quiz item {index} has an answer outside its choices")
    for index, row in enumerate(topic["problems"]):
        for key in ("number", "title", "container", "pattern", "stdlib", "why"):
            if key not in row:
                raise ContentError(f"{source}: problem {index} is missing {key}")


def readme(topic: dict) -> str:
    lines = [f"# {topic['title']}", "", "> Generated from `content/`. Edit the YAML, then run `tools/build.py`.", ""]
    lines += [topic["summary"].strip(), ""]
    for part in topic["mechanics"]:
        lines += [f"## {part['heading']}", "", part["body"].strip(), ""]
    lines += ["## Complexity", "", "| Operation | Time | Note |", "| --- | --- | --- |"]
    lines += [f"| `{row['operation']}` | {row['time']} | {row['note']} |" for row in topic["complexity"]]
    lines += [
        "",
        "## Signal to structure",
        "",
        "| Signal in the problem | Requirement | Structure | Python tool | Example |",
    ]
    lines += ["| --- | --- | --- | --- | --- |"]
    lines += [
        f"| {row['signal']} | {row['requirement']} | {row['structure']} | `{row['stdlib']}` | {row['example']} |"
        for row in topic["signals"]
    ]
    lines += ["", "## Problems mapped to this topic", ""]
    lines += ["| Problem | Container | Pattern | Python tool | Why |", "| --- | --- | --- | --- | --- |"]
    lines += [
        f"| LeetCode {row['number']} {row['title']} | {row['container']} | {row['pattern']} | `{row['stdlib']}` | {row['why']} |"
        for row in topic["problems"]
    ]
    lines += ["", "## Claims and their checks", ""]
    lines += [f"- `{claim['id']}`: {claim['text']}" for claim in topic["claims"]]
    return "\n".join(lines).rstrip("\n") + "\n"


def quiz_guide(topic: dict) -> str:
    lines = [f"# Quiz: {topic['title']}", "", "> Generated from `content/`.", ""]
    for number, item in enumerate(topic["quiz"], start=1):
        lines += [f"## {number}. {item['question']}", ""]
        lines += [f"{letter}. {choice}" for letter, choice in zip("ABCDEFGH", item["choices"], strict=False)]
        answer = "ABCDEFGH"[item["answer"]]
        lines += ["", f"**Answer: {answer}.** {item['explanation']}", ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def index_html(topic: dict) -> str:
    esc = html.escape
    parts = [
        "<!doctype html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(topic['title'])}</title>",
        "<style>body{font-family:system-ui,sans-serif;max-width:52rem;margin:2rem auto;padding:0 1rem;line-height:1.5}"
        "table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:.4rem;text-align:left;vertical-align:top}"
        "code{background:#f3f3f3;padding:0 .2rem}</style>",
        "</head><body>",
        f"<h1>{esc(topic['title'])}</h1>",
        f"<p>{esc(topic['summary'].strip())}</p>",
    ]
    for part in topic["mechanics"]:
        parts.append(f"<h2>{esc(part['heading'])}</h2><p>{esc(part['body'].strip())}</p>")
    parts.append("<h2>Complexity</h2><table><tr><th>Operation</th><th>Time</th><th>Note</th></tr>")
    parts += [
        f"<tr><td><code>{esc(r['operation'])}</code></td><td>{esc(r['time'])}</td><td>{esc(r['note'])}</td></tr>"
        for r in topic["complexity"]
    ]
    parts.append("</table><h2>Signal to structure</h2><table><tr><th>Signal</th><th>Requirement</th>")
    parts.append("<th>Structure</th><th>Python tool</th><th>Example</th></tr>")
    parts += [
        f"<tr><td>{esc(r['signal'])}</td><td>{esc(r['requirement'])}</td><td>{esc(r['structure'])}</td>"
        f"<td><code>{esc(r['stdlib'])}</code></td><td>{esc(r['example'])}</td></tr>"
        for r in topic["signals"]
    ]
    parts.append("</table><h2>Problems</h2><table><tr><th>Problem</th><th>Container</th><th>Pattern</th>")
    parts.append("<th>Python tool</th><th>Why</th></tr>")
    parts += [
        f"<tr><td>LeetCode {r['number']} {esc(r['title'])}</td><td>{esc(r['container'])}</td><td>{esc(r['pattern'])}</td>"
        f"<td><code>{esc(r['stdlib'])}</code></td><td>{esc(r['why'])}</td></tr>"
        for r in topic["problems"]
    ]
    parts.append("</table></body></html>")
    return "\n".join(parts) + "\n"


def flashcards(topics: list[dict]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    for topic in topics:
        for item in topic["quiz"]:
            answer = item["choices"][item["answer"]]
            writer.writerow([item["question"], f"{answer}. {item['explanation']}", topic["id"]])
        for row in topic["complexity"]:
            writer.writerow([f"Time complexity of {row['operation']}?", row["time"], f"{topic['id']} complexity"])
    return buffer.getvalue()


def render_all(content_dir: Path = CONTENT) -> dict[Path, str]:
    """Every generated file, keyed by its path under the family root. Pure: writes nothing."""
    topics = load_topics(content_dir)
    outputs: dict[Path, str] = {}
    for topic in topics:
        stem = topic["id"]
        outputs[Path(f"{stem}/README.md")] = readme(topic)
        outputs[Path(f"{stem}/quiz_guide.md")] = quiz_guide(topic)
        outputs[Path(f"{stem}/index.html")] = index_html(topic)
    outputs[Path("flashcards.csv")] = flashcards(topics)
    return outputs


def write_all(root: Path = ROOT) -> list[Path]:
    written = []
    for relative, text in render_all().items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        _ = target.write_text(text, encoding="utf-8")
        written.append(target)
    return written


if __name__ == "__main__":
    for path in write_all():
        print(f"wrote {path.relative_to(ROOT.parent)}")
