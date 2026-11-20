# Quiz: Visitor

> Generated from `content/`.

## 1. Visitor is a good fit when:

A. Element types change frequently but operations are fixed
B. Element structure is stable and new operations are added often
C. You need to share intrinsic state
D. You need runtime service discovery

**Answer: B.** It optimizes for adding operations across a stable set of elements.

## 2. A major cost of Visitor is:

A. No way to group operation logic
B. Adding a new element type forces updates to all visitors
C. It cannot traverse structures
D. It requires global variables

**Answer: B.** The visitor interface mirrors the element hierarchy.
