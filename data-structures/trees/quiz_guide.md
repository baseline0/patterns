# Quiz: Binary trees and BSTs: traversal, recursion, and tree properties

> Generated from `content/`.

## 1. Why is recursion a natural fit for tree problems?

A. Trees are always small, so recursion never overflows
B. Each subtree is a smaller instance of the same problem, making induction natural
C. Recursion is faster than iteration
D. Trees require random access, which recursion provides

**Answer: B.** The recursive structure of a tree (subtree is a tree) matches the recursive structure of the solution (solve left, right, combine).

## 2. What does in-order traversal of a BST produce?

A. Nodes in reverse sorted order
B. Nodes sorted from smallest to largest
C. Nodes in the order they were inserted
D. Nodes in reverse insertion order

**Answer: B.** In-order traversal visits left subtree, then node, then right subtree. In a BST, left nodes are smaller, so the result is sorted.

## 3. Why does BST search run in O(log n) time on a balanced tree but O(n) on an unbalanced tree?

A. Unbalanced trees store data differently
B. Unbalanced trees require random access
C. A balanced tree eliminates about half the tree per comparison; an unbalanced tree may eliminate only one node
D. Unbalanced trees require more memory

**Answer: C.** On a balanced tree, comparison with the root partitions the remaining nodes. On a chain (unbalanced), only one node is eliminated per step.

## 4. Which traversal naturally uses a queue instead of recursion?

A. Pre-order (depth-first)
B. In-order (depth-first)
C. Level-order (breadth-first)
D. Post-order (depth-first)

**Answer: C.** Level-order visits nodes by depth, layer by layer, which a queue enforces naturally. DFS traversals use recursion or a stack.

## 5. What invariant must a BST maintain?

A. Left children are smaller, right children are larger
B. All nodes at each level are sorted
C. The tree is always perfectly balanced
D. Child values are the average of their parent and sibling

**Answer: A.** In a BST, every node must have smaller values in its left subtree and larger values in its right subtree.
