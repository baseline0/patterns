"""Terminal quiz built from the same YAML as the written guide. Answer with the letter of a choice; press Ctrl-C to stop."""

from __future__ import annotations

from build import load_topics


def ask(item: dict) -> bool:
    print(f"\n{item['question']}")
    letters = "ABCDEFGH"
    for letter, choice in zip(letters, item["choices"], strict=False):
        print(f"  {letter}. {choice}")
    reply = input("Your answer: ").strip().upper()
    correct = letters[item["answer"]]
    if reply == correct:
        print("Correct.")
        return True
    print(f"Not quite: the answer is {correct}. {item['explanation']}")
    return False


def run() -> int:
    items = [(topic["title"], item) for topic in load_topics() for item in topic["quiz"]]
    score = 0
    try:
        for title, item in items:
            print(f"\n[{title}]")
            score += ask(item)
    except (KeyboardInterrupt, EOFError):
        print()
    print(f"\nScore: {score} of {len(items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
