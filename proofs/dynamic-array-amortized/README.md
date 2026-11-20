# Dynamic array append is amortized O(1)

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Statement**: A sequence of n appends to a geometrically growing array costs O(n) time in total.

**Invariant**: After every append, capacity is at least length; immediately after a resize, capacity is at most twice length.

## Steps

- **Base case**: The first append writes one slot into the initial capacity and performs no copy.
- **Resize points form a geometric series** (depends on base): Capacity doubles only when length reaches capacity, so resizes happen at lengths 1, 2, 4, 8, and so on.
- **Total copy work is bounded** (depends on doubling): Across all resizes the array copies at most 1 + 2 + 4 + ... + n slots, which is less than 2n.
- **Add writes and copies** (depends on copies): n appends perform n writes and fewer than 2n copies, so the sequence is linear and each append is O(1) on average.

**Complexity**: O(n) for n appends; O(1) amortized, O(n) worst case for a single resize.

## Explore

- Searchable local catalogue: `just -f site/justfile serve` then open `site/index.html`.

## Linked claims

- `list-append-is-amortized-constant`
