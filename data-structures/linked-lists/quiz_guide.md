# Quiz: Linked lists: pointers, reversal, and cycle detection

> Generated from `content/`.

## 1. Why is reversal a natural fit for linked lists?

A. Linked lists are smaller than arrays
B. Pointers can be redirected in-place without allocating new nodes, using O(1) extra space
C. Reversing arrays requires copying the entire array
D. Linked lists are always bidirectional

**Answer: B.** Reversing a linked list changes the direction of pointers, not the nodes themselves. This in-place redirection uses constant extra space.

## 2. How does the two-pointer cycle detection algorithm work?

A. Mark visited nodes with a flag
B. Use a set to track seen nodes
C. Advance two pointers at different speeds; they meet if a cycle exists
D. Count nodes and check if the count exceeds the list length

**Answer: C.** A fast pointer (2 steps per iteration) and a slow pointer (1 step) eventually meet if a cycle exists. If the fast pointer reaches null, there is no cycle.

## 3. Why is a dummy node useful when merging linked lists?

A. It makes the list shorter
B. It holds the smaller of the two heads
C. It eliminates special cases at the head by providing a node to attach to initially
D. It is required by the algorithm

**Answer: C.** A dummy node lets the merge code treat the head uniformly. Instead of checking 'is this the first node?', the code always attaches to the previous node.

## 4. In the 'Merge K Sorted Lists' problem, why is a heap faster than pairwise merging?

A. Heaps use less memory
B. Heaps sort the lists automatically
C. Finding the next smallest among k lists is O(log k) with a heap instead of O(k) with linear search
D. Heaps eliminate the need for pointers

**Answer: C.** A heap tracks the smallest head across k lists. Inserting and extracting takes O(log k) per step, making the total time O(n log k) instead of O(n * k).

## 5. What is the time complexity of traversing a linked list to find a specific node?

A. O(1)
B. O(log n)
C. O(n)
D. O(n log n)

**Answer: C.** A linked list has no random access. Reaching a node requires following pointers from the head, which takes O(n) in the worst case.
