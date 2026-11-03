# Quiz: Heaps: a priority queue in a flat list

> Generated from `content/`.

## 1. Why does heapq store a heap in a plain list?

A. Lists are the only mutable sequence in Python
B. The children of index i are at 2i+1 and 2i+2, so no node objects are needed
C. heapq only works on tuples
D. A heap is faster to store as a list because it stays sorted

**Answer: B.** The array layout gives the tree's parent and child positions by arithmetic, with no pointers to manage.

## 2. What is the cost of heapq.heappop on a heap of n items?

A. O(1)
B. O(log n)
C. O(n)
D. O(n log n)

**Answer: B.** The last item moves to the root and sifts down at most one path, about log n levels.

## 3. heapq is a min-heap. How do you get the largest value first?

A. Call heapq.heappop(max=True)
B. Push the negated values and pop the smallest
C. Sort the list first
D. Use a deque instead

**Answer: B.** The most negative number is the one with the largest magnitude, so negating turns max into min.

## 4. Why is building a heap from a list with heapify faster than n heappush calls?

A. heapify skips the comparisons
B. heapify is O(n) bottom-up, while n pushes cost O(n log n) in total
C. heappush cannot be used on lists
D. heapify sorts the list first

**Answer: B.** Sifting down from the middle does less total work than sifting up each item as it arrives.
