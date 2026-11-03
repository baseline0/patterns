# Quiz: Lists and deques: contiguous arrays versus block lists

> Generated from `content/`.

## 1. Why is list.pop(0) a poor choice for a BFS queue?

A. It allocates a new list every time
B. It shifts every remaining pointer, so each pop costs O(n)
C. It is not allowed on lists
D. It is only slow for strings

**Answer: B.** A list is a contiguous array. Removing the first element moves each remaining pointer one slot left.

## 2. Which structure is the right queue for BFS in Python?

A. list with pop(0)
B. collections.deque with popleft
C. dict with the smallest key
D. set with pop()

**Answer: B.** deque.popleft is O(1), because it touches only the block at the front.

## 3. Why are appends to a list amortized O(1)?

A. Each append reserves exactly one slot
B. Capacity grows by a fraction each time it is exceeded, so copies are rare
C. Appends never copy
D. CPython stores lists as linked nodes

**Answer: B.** Spare capacity grows geometrically, so the cost of the occasional copy spreads across many appends.

## 4. bisect.insort on a sorted list is O(log n) per insert. True or false?

A. True: the binary search dominates
B. False: the search is O(log n) but the list shift makes insertion O(n)

**Answer: B.** Finding the position is logarithmic. Inserting the value shifts the elements after it.

## 5. Why can a list not be a dict key?

A. Lists are too large
B. Lists are not hashable: their contents can change, so their hash would change too
C. Dict keys must be strings
D. Lists are stored out of order

**Answer: B.** A key's hash must stay constant while it is in the table. A mutable list cannot guarantee that.
