# Bottom-up heapify is linear

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

**Statement**: Constructing a binary heap by calling sift-down from the last internal node to the root takes O(n) time.

**Invariant**: Before node i is processed, every subtree rooted at an index greater than i is already a valid heap.

## Steps

- **Leaves are heaps**: Nodes with no children already satisfy the heap property, so processing can start at the last parent.
- **Process internal nodes bottom-up** (depends on leaves): Walking from the last parent down to the root guarantees each child subtree is a heap before its parent is fixed.
- **Cost depends on height** (depends on reverse): A node at height h moves at most h levels, and a binary heap has at most ceil(n / 2^(h+1)) nodes at height h.
- **Bound the weighted sum** (depends on height-cost): The sum over heights of h * n / 2^(h+1) is at most n, because the series sum h / 2^h converges to 2.

**Complexity**: O(n) time and O(1) extra space, versus O(n log n) for repeated insertion.

## Explore

- Open in explorer: `../../site/index.html#proofs:proof:heapify-linear` (`just -f site/justfile serve`)

## Linked claims

- `heapify-is-linear`
