"""Check that commits being pushed do not carry Co-Authored-By trailers.

Used by just/repo-push.just. Exits non-zero if any commit in the range contains a
Co-authored-by trailer.
"""

from __future__ import annotations

import subprocess
import sys


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    repo = "."
    rev_range: str | None = None
    allow = False

    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--repo" and index + 1 < len(argv):
            repo = argv[index + 1]
            index += 2
        elif arg == "--range" and index + 1 < len(argv):
            rev_range = argv[index + 1]
            index += 2
        elif arg == "--allow-co-authored-by":
            allow = True
            index += 1
        else:
            index += 1

    if allow:
        return 0
    if not rev_range:
        print("missing --range", file=sys.stderr)
        return 2

    try:
        result = subprocess.run(
            ["git", "-C", repo, "log", "--format=%B%x00", rev_range],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.strip() or "failed to read commit range", file=sys.stderr)
        return exc.returncode or 1

    messages = [message for message in result.stdout.split("\x00") if message.strip()]
    bad: list[str] = []
    for message in messages:
        for line in message.splitlines():
            if line.lower().startswith("co-authored-by:"):
                bad.append(line.strip())
                break
    if bad:
        print("[!] refuse: commits in range contain Co-Authored-By trailer(s):", file=sys.stderr)
        for line in bad:
            print(f"    {line}", file=sys.stderr)
        print(
            "[*] Reword commits to remove trailers, or rerun with an explicit override if supported.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
