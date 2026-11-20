# Sliding window moves each pointer at most n times

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Statement**: A sliding window over an array of n elements runs in O(n) time when each pointer only moves forward.

**Invariant**: At the start of every iteration the half-open interval [left, right) is the current window and right is one past the last inspected element.

## Steps

- **Empty window**: Set left = right = 0. The window is empty and the invariant holds before any input is consumed.
- **Right pointer only advances** (depends on init): Each iteration admits at most one new element by increasing right, so right advances at most n times.
- **Left pointer only advances** (depends on init): Invalid windows are repaired by increasing left; it never decreases, so left also advances at most n times.
- **Sum the pointer moves** (depends on expand, shrink): At most n expansions plus at most n shrink steps gives O(n) total work, with O(1) extra space.

**Complexity**: O(n) time, O(1) extra space.

## Linked claims

- `sliding-window-is-linear`
