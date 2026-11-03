# Lists and deques: contiguous arrays versus block lists

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

A Python list is a contiguous array of object pointers that grows geometrically. A deque is a chain of fixed-size blocks, so both of its ends are cheap to change. Choosing between them is a question about where a container changes.

## list: a contiguous array of pointers

A list stores pointers to objects, not the objects themselves. Appending writes into spare capacity. When the spare capacity runs out, CPython allocates a larger array and copies the pointers across. The new capacity is about 1/8 larger plus a small constant, so copies are rare and the average append stays constant (amortized O(1)).

## deque: a chain of fixed-size blocks

A deque is a doubly linked chain of blocks, each holding 64 pointers. Operations at either end touch only the block at that end, so popleft and appendleft are O(1). Reaching the middle means walking blocks, so indexing is linear in the position, not constant.

## why list.pop(0) is the trap

Removing the first element of a list shifts every remaining pointer one slot left. The cost grows with the length of the list. Used as a FIFO queue in a loop, it turns a linear traversal into quadratic work.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `list.append` | O(1) amortized | geometric growth of spare capacity |
| `list.pop()  (end)` | O(1) |  |
| `list.pop(0) / insert(0, x)` | O(n) | every pointer shifts |
| `list[i]` | O(1) | direct offset into the array |
| `deque.appendleft / popleft` | O(1) | touches only the end block |
| `deque[i] (middle)` | O(n) | walks blocks; not constant |
| `bisect.bisect_left (search)` | O(log n) | on a sorted list |
| `bisect.insort (insert)` | O(n) | the search is O(log n); the shift is linear |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Process in first-in, first-out order, with work added and removed at both ends | O(1) at both ends | block list | `collections.deque` | Binary Tree Level Order Traversal (LeetCode 102) |
| Last-in, first-out; nearest greater or smaller element in one pass | O(1) push and pop at one end; O(n) total | contiguous array used as a stack | `list (append / pop)` | Daily Temperatures (LeetCode 739) |
| Maintain a sorted sequence while looking values up | O(log n) search; insertion dominated by the shift | sorted contiguous array | `bisect` | Searching a sorted list; avoid repeated insort in hot loops |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| LeetCode 102 Binary Tree Level Order Traversal | block list (deque) | breadth-first search | `collections.deque: append and popleft` | The frontier is a FIFO queue. list.pop(0) would shift the whole frontier on every step. |
| LeetCode 739 Daily Temperatures | contiguous array (list) | monotonic stack | `list: append and pop` | The stack is used only at one end, so a plain list costs O(1) per push and pop. |
| LeetCode 11 Container With Most Water | contiguous array (list) | two pointers | `list indexing` | Random access by position is O(1), which the two pointers rely on. |

## Claims and their checks

- `list-append-is-amortized-constant`: List growth is geometric: capacity grows by a bounded fraction each time it is exceeded, so appends stay O(1) amortized.
- `list-pop-zero-scales-linearly`: list.pop(0) cost grows with the list length, because every remaining pointer shifts.
- `deque-popleft-is-constant`: deque.popleft cost does not grow with the deque length.
- `insort-shift-is-linear`: bisect.insort is a binary search plus a list shift, so insertion at the front is linear; the search alone is logarithmic.
- `dict-keys-must-be-hashable`: A dict key must be hashable. A list is not hashable, so it cannot be a key.
- `dict-preserves-insertion-order`: dict iteration follows insertion order (a language guarantee since Python 3.7).
