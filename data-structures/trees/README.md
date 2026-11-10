# Binary trees and BSTs: traversal, recursion, and tree properties

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

A tree is a directed acyclic graph where each node (except the root) has one parent. A binary tree restricts each node to at most two children. A binary search tree adds the invariant that left descendants are smaller and right descendants are larger, making search and insertion natural recursive tasks. Tree problems are solved by recognizing that each subtree is a smaller instance of the same problem.

## recursive structure: each subtree is a tree

The key insight is that a subtree rooted at any node is itself a tree. This recursive structure makes induction natural. A function that solves the problem for a subtree can solve it for any tree by calling itself on the left and right children, then combining the results. Recursion eliminates explicit stack management for many tree problems.

## search in a BST: left is smaller, right is larger

A BST maintains the invariant: every node in the left subtree is smaller, every node in the right subtree is larger. This allows search to eliminate half the tree at each step, giving O(log n) search on a balanced tree. Insertion and deletion maintain the invariant by choosing a branch based on the comparison.

## traversal orders: pre, in, post, level

Pre-order visits the node before its children (node-left-right). In-order visits the left subtree, then the node, then the right subtree (left-node-right); on a BST this yields sorted order. Post-order visits children before the node (left-right-node), useful for deletion. Level-order visits nodes by depth, layer by layer, and naturally uses a queue instead of recursion.

## recursive vs. iterative traversal

Recursion is elegant and matches the problem structure, but it uses stack space proportional to tree height. An iterative traversal uses an explicit stack (or deque for level-order) and avoids recursion limits. The choice depends on the tree depth and whether recursion clarity matters more than stack efficiency.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `BST search (balanced)` | O(log n) | each comparison halves the tree; unbalanced tree degrades to O(n) |
| `BST insert (balanced)` | O(log n) | search for the position, then add a leaf |
| `BST delete (balanced)` | O(log n) | search, then restructure; unbalanced tree O(n) |
| `Tree traversal (DFS pre/in/post)` | O(n) | visit every node and edge once; recursive depth is O(h) |
| `Tree traversal (BFS level-order)` | O(n) | deque maintains the frontier; space is O(w) where w is max width |
| `Find LCA (lowest common ancestor)` | O(n) | search both subtrees to find the split point; O(h) on a balanced tree |
| `Validate BST` | O(n) | check every node's invariant and track bounds |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Check if two trees have the same structure and values | Compare recursively; O(n) in worst case | recursive comparison | `recursion; compare left and right subtrees` | Same Tree (LeetCode 100) |
| Find maximum depth or path length from root | Recurse to each leaf and combine results | post-order recursion | `recursion on left and right subtrees` | Maximum Depth of Binary Tree (LeetCode 104) |
| Verify that a tree satisfies BST properties at every node | Track bounds; no value escapes left < node < right | recursive validation with min/max bounds | `recursion; pass down constraints` | Validate Binary Search Tree (LeetCode 98) |
| Collect results from each level of the tree | Visit all nodes at depth d before depth d+1 | breadth-first with a queue | `collections.deque; append and popleft` | Binary Tree Level Order Traversal (LeetCode 102) |
| Find paths or relationships between nodes in the tree | Locate common ancestor or nearest node in sorted order | recursive search with context | `recursion; track path or constraint` | Lowest Common Ancestor (LeetCode 236) |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| LeetCode 100 Same Tree | recursive tree comparison | structural equality check | `recursion; compare node values and recurse on subtrees` | Two trees are the same if their roots have equal values and both subtrees are identical. Recursion naturally expresses this. |
| LeetCode 104 Maximum Depth of Binary Tree | recursive depth computation | post-order traversal | `recursion; max(depth(left), depth(right)) + 1` | Depth of a tree is one plus the maximum depth of its subtrees. Recursion unwraps this definition. |
| LeetCode 98 Validate Binary Search Tree | recursive BST validation with bounds | constrained recursion | `recursion; pass min and max bounds down the tree` | A BST must satisfy bounds at every node. Recursion tracks constraints: left subtree < node < right subtree. |
| LeetCode 102 Binary Tree Level Order Traversal | breadth-first search with deque | level-order traversal | `collections.deque; append children, popleft to process` | Level-order requires visiting all nodes at depth d before depth d+1, which a queue naturally provides. |
| LeetCode 105 Construct Binary Tree from Preorder and Inorder Traversal | recursive tree reconstruction | divideandconquer via traversal properties | `recursion; preorder gives root, inorder partitions left/right` | Preorder starts with the root. Inorder shows which nodes are left and right. Recursion reconstructs subtrees. |
| LeetCode 236 Lowest Common Ancestor of a Binary Tree | recursive ancestor search | postorder traversal for result aggregation | `recursion; check left and right subtrees, return non-null result` | The LCA is the deepest node that has both targets as descendants. Recursion finds it by returning the first non-null result. |
| LeetCode 543 Diameter of Binary Tree | recursive path length computation | postorder traversal tracking global max | `recursion; track height and update max diameter` | The diameter passes through some node as the longest path from left to right. Recursion computes heights and tracks the max sum. |

## Claims and their checks

- `tree-is-recursive-structure`: A binary tree is defined recursively: a node with a left and right subtree, each of which is a binary tree (or empty).
- `bst-maintains-invariant`: A binary search tree maintains the invariant that every left descendant is smaller and every right descendant is larger.
- `inorder-traversal-yields-sorted`: In-order traversal of a BST visits nodes in sorted order.
- `tree-height-bounds-recursive-depth`: The height of a tree bounds the recursion depth and the required stack space.
- `balanced-tree-search-is-logarithmic`: Search in a balanced BST takes O(log n) time because each comparison eliminates about half the tree.
