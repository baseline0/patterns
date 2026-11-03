# Heaps: a priority queue in a flat list

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

heapq keeps a binary heap inside an ordinary list. The smallest element is always at index 0, so reading it is O(1); insertion and removal are O(log n). It is the standard tool when a problem asks for the next smallest or largest element while the data keeps changing.

## a binary heap in a flat array

A heap is a complete binary tree stored level by level in a list. The children of index i sit at 2i+1 and 2i+2, and the parent of i sits at (i-1)//2. heapq maintains the min-heap rule: every parent is no larger than its children, so the minimum is at index 0.

## push and pop move one path

heappush appends the item and sifts it up past larger parents, at most log n steps. heappop removes index 0, moves the last item to the root, and sifts it down, again at most log n steps. Neither touches the whole list.

## heapify builds a heap in linear time

heapq.heapify restructures an existing list in place, sifting down from the middle. Building a heap this way is O(n), cheaper than n pushes. A max-heap is a min-heap of negated values, since heapq has no max-heap mode.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `heap[0] (peek minimum)` | O(1) | the minimum is always at index 0 |
| `heapq.heappush` | O(log n) | sift up at most log n levels |
| `heapq.heappop` | O(log n) | move the last item to the root, sift down |
| `heapq.heapify` | O(n) | bottom-up, in place |
| `heapq.nlargest(k, data)` | O(n log k) | keeps a heap of size k while scanning |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Find the k largest or smallest elements in a stream or a large list | O(n log k), with only k items held | binary heap of size k | `heapq (heappush / heappop) or heapq.nlargest` | Top K Frequent Elements (LeetCode 347) |
| Repeatedly take the two smallest and combine them | O(log n) per step, the smallest always available | binary heap | `heapq` | Minimum Cost to Connect Sticks (LeetCode 1167) |
| Merge several sorted sequences in order | O(N log k) for N items from k sources | heap of one head per source | `heapq.merge` | Merge k Sorted Lists (LeetCode 23) |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| LeetCode 347 Top K Frequent Elements | binary heap (heapq) | top-k selection | `collections.Counter, then heapq.nlargest` | Only the k most frequent matter, so a heap of size k beats sorting every distinct value. |
| LeetCode 215 Kth Largest Element in an Array | binary heap of size k | top-k selection | `heapq: heappush, and heappop when the heap grows past k` | A min-heap of the k largest seen so far keeps its root as the answer. |
| LeetCode 23 Merge k Sorted Lists | binary heap of list heads | k-way merge | `heapq.heappush / heappop, or heapq.merge` | One head per list in the heap gives the next smallest value across all lists in O(log k). |

## Claims and their checks

- `heap-root-is-minimum`: After heapq.heapify, the first element of the plain list is the minimum.
- `heappop-yields-sorted-order`: Repeated heappop returns the elements in ascending order.
- `heapify-is-linear`: heapify on n items costs about n, not n log n: doubling n roughly doubles the time, not more.
- `nlargest-beats-a-full-sort-for-small-k`: heapq.nlargest(k, data) for small k is faster than sorting all of data and slicing.
