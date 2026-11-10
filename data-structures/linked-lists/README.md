# Linked lists: pointers, reversal, and cycle detection

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

A linked list chains nodes together with pointers, so insertion and deletion at a known position cost O(1). The price is that reaching a position requires walking from the head, which costs O(n). Linked list problems are solved by careful pointer manipulation: maintaining two pointers to track state, reversing in-place by redirecting links, or detecting cycles by observing that two pointers moving at different speeds must meet if a cycle exists.

## node-based structure: pointer chaining

Each node holds a value and a pointer to the next node. Unlike arrays, there is no random access; reaching a node requires starting at the head and following pointers. This sequential access makes insertion and deletion at a known position cheap (no shifting), but finding a position is expensive (no binary search).

## reversal: redirect pointers in-place

To reverse a linked list, redirect each node's pointer to point backward instead of forward. Iterate through the list, keeping track of the previous node. At each step, change the current node's pointer from next to previous, then advance. This reverses the chain in-place without allocating new nodes, using O(1) extra space.

## cycle detection: two pointers at different speeds

If a list has a cycle, a fast pointer (advancing 2 steps per iteration) and a slow pointer (advancing 1 step) will eventually meet. If the fast pointer reaches null, there is no cycle. Once a cycle is found, the distance from the head to the cycle entry equals the distance from the meeting point back to the entry, a fact that allows finding the cycle start.

## merging and multi-pointer patterns

Many linked list problems require tracking multiple pointers simultaneously: a dummy node simplifies edge cases at the head, a fast and slow pointer find the middle, or two pointers track positions in different lists. Careful pointer management avoids breaking the chain or creating dangling references.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `Traverse the list (find a node)` | O(n) | must follow pointers from the head |
| `Insert at a known position (with a pointer to the previous node)` | O(1) | redirect two pointers, no shifting |
| `Delete at a known position (with a pointer to the previous node)` | O(1) | redirect one pointer, no shifting |
| `Reverse the entire list` | O(n) | one pass, redirecting pointers; O(1) extra space |
| `Detect a cycle` | O(n) | fast and slow pointers; they meet if a cycle exists |
| `Merge two sorted lists` | O(n + m) | compare nodes from both lists, advance the smaller |
| `Merge k sorted lists (naive)` | O(n * k^2) | merge pairwise; improve with a heap or merge sort strategy |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Reverse a sequence when you cannot use an array | Change direction in-place; O(n) time | pointer redirection in a single pass | `manual pointer management` | Reverse Linked List (LeetCode 206) |
| Detect or break a cycle in a chain | Identify loops without extra space or mutation | two-pointer race: fast and slow | `two pointer variables` | Linked List Cycle (LeetCode 141) |
| Merge multiple sequences while maintaining order | Compare heads, advance the smaller, O(n + m) for two lists | pointer manipulation with a dummy node | `manual pointer chaining` | Merge Two Sorted Lists (LeetCode 21) |
| Find the middle of a list or reverse a section | Locate a position without knowing the length | two pointers: one moves 2 steps, one moves 1 | `two pointer variables; count or fast/slow` | Reverse Linked List II (LeetCode 92) |
| Simulate addition with numbers stored as linked list nodes | Process digit by digit with carry; may need to extend the list | traverse both lists in parallel, manage carry state | `manual pointer advancement and node creation` | Add Two Numbers (LeetCode 2) |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| LeetCode 206 Reverse Linked List | pointer redirection in-place | iterative pointer reversal | `manual pointer management; track previous, current, next` | Reversing requires redirecting each node's pointer from forward to backward. Tracking three pointers (prev, curr, next) allows safe redirection in one pass. |
| LeetCode 141 Linked List Cycle | two-pointer cycle detection | tortoise and hare | `two pointer variables advancing at different speeds` | If a cycle exists, two pointers at different speeds must meet. If the fast pointer reaches null, there is no cycle. |
| LeetCode 21 Merge Two Sorted Lists | pointer-based merge with dummy node | two-pointer list merging | `dummy node, manual pointer chaining` | Merging compares heads and advances the smaller pointer. A dummy node avoids special-casing the new head. |
| LeetCode 23 Merge K Sorted Lists | heap-based or divide-and-conquer merging | reduce k lists to 1 via pairwise merging | `heapq.heappush for efficient next-smallest, or recursion` | Naive pairwise merging is slow; a heap picks the next smallest in O(log k) time, making total time O(n log k). |
| LeetCode 92 Reverse Linked List II | pointer redirection in a range | bounded reversal | `manual pointer management; track boundaries` | Reversing only a section requires finding the start, reversing in place, then connecting back. Careful pointer tracking avoids breaking the chain. |
| LeetCode 2 Add Two Numbers | parallel node traversal with carry | digit-by-digit addition | `manual pointer advancement, node creation` | Addition processes digits in parallel, managing carry state. New nodes are created for the result; careful pointer management avoids leaks. |
| LeetCode 160 Intersection of Two Linked Lists | two-pointer convergence | length-adjusted pointers | `manual pointer advancement; two passes to align` | If two lists intersect, advancing through both at equal speed detects the intersection. Equal-length traversal aligns the pointers. |

## Claims and their checks

- `linked-list-no-random-access`: A linked list requires O(n) steps to reach a position, so binary search is impossible without modifying the structure.
- `linked-list-insert-delete-constant`: Insertion and deletion at a known node (with a pointer to it) cost O(1), because no shifting is required.
- `reversal-redirects-pointers-inplace`: Reversing a linked list in-place by redirecting pointers uses O(1) extra space and O(n) time.
- `cycle-detection-two-pointers`: A cycle in a linked list can be detected by advancing two pointers at different speeds; if they meet, a cycle exists.
- `dummy-node-simplifies-head-cases`: A dummy node pointing to the head eliminates special cases when modifying the head node.
