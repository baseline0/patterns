# Arrays and 2D arrays: subarrays, sliding window, and in-place operations

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Open in explorer: `../../site/index.html#data-structures:data-structure:arrays-and-2d-arrays` (`just -f site/justfile serve`)

Arrays store elements in contiguous memory for O(1) indexing. Subarrays are contiguous ranges; sliding windows and prefix sums solve subarray problems in linear time. Two pointers on sorted arrays find pairs without nested loops. In-place operations on 2D arrays avoid allocating new matrices by using index algebra and element swaps.

## sliding window for subarray conditions

Two pointers bound a window. The right pointer expands to add elements; the left contracts to maintain a condition (max length, sum within range, no repeats). Each element is added and removed once, keeping work linear.

## prefix sums for constant-time range queries

A prefix sum array stores cumulative totals at each position. Any subarray sum can be computed in O(1) using prefix[end] - prefix[start-1]. This trades O(n) preprocessing for O(1) per query.

## two pointers converging toward a target

Two pointers at opposite ends move inward toward a target. If the sum is too small, move the left pointer right (increase sum); if too large, move the right pointer left (decrease sum). This solves two-sum and k-sum problems in O(n) on sorted arrays.

## in-place matrix operations via index algebra

Rotating and spiraling through a matrix in place uses index transformations and element swaps. Tracking layer boundaries or computing new positions avoids allocating new matrices.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `subarray sum (all pairs, brute force)` | O(n^2) | nested loop over start and end indices |
| `subarray sum (prefix sum query)` | O(n) setup, O(1) per query | cumulative total lookup |
| `sliding window (max in subarray, longest substring)` | O(n) | each element added and removed once |
| `two sum (sorted array)` | O(n) | two pointers converge to target |
| `three sum (brute force)` | O(n^3) | three nested loops |
| `three sum (sorted + two pointers)` | O(n^2) | fix one element, use two pointers for complement |
| `rotate matrix 90 degrees in place` | O(n^2) and O(1) space | transpose and reverse, or rotate layers |
| `spiral matrix traversal` | O(n*m) and O(1) space | track four boundaries; visit each cell once |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Find the subarray with max sum, longest run, or extreme property | O(n) without nested loops | sliding window or dynamic programming | `list indexing and two pointers` | Maximum Subarray (LeetCode 53); Kadane's algorithm |
| Find all pairs or triplets that satisfy a constraint (sum to target, meet criteria) | O(n) or O(n^2) without O(n^3) brute force | two pointers on sorted array; hash set for complements | `set or dict for Two Sum; sort then two pointers for k-sum` | Two Sum (LeetCode 1); 3Sum (LeetCode 15) |
| Answer range queries on subarrays (sum, product, max, min, count) | O(1) per query after preprocessing | prefix or suffix array (cumulative aggregation) | `list with cumulative values` | Product of Array Except Self (LeetCode 238); Range Sum Query |
| Manipulate a 2D matrix without allocating new space | O(1) extra space, no new matrix allocation | in-place index transformations and swaps | `list of lists, index arithmetic` | Rotate Matrix (LeetCode 48); Spiral Matrix (LeetCode 54) |
| Maximize or minimize a value between two positions | O(n) without enumerating all pairs | two pointers or one-pass greedy | `list indexing and comparison` | Container With Most Water (LeetCode 11); Trapping Rain Water |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| LeetCode 1 Two Sum | hash table (dict) | complement lookup in one pass | `dict to store value-index pairs; check for target - current` | Complement lookup is O(1), so one pass finds the pair without sorting. Hash table avoids O(n^2) nested loops. |
| LeetCode 11 Container With Most Water | contiguous array | two pointers from ends moving inward | `list indexing; compute area = height * width` | Area is limited by the shorter height. Moving from the widest pair inward, we skip impossible pairs in O(n) instead of O(n^2). |
| LeetCode 15 3Sum | sorted array | fix one element, use two pointers for complement | `sort once, then two pointers for each fixed element` | Fixing each element and solving two-sum with two pointers reduces O(n^3) brute force to O(n^2) after sorting. |
| LeetCode 53 Maximum Subarray | contiguous array | Kadane's algorithm (track max ending here and global max) | `single-pass loop with running sum` | At each position, choose: extend the previous subarray or start new. Tracking both maxima finds the best in O(n). |
| LeetCode 238 Product of Array Except Self | prefix and suffix product arrays | left products, right products, combine | `two passes over the array; no division` | Division by zero is avoided. Left products (all before i) and right products (all after i) multiply to the result. O(n) without division. |
| LeetCode 48 Rotate Matrix | 2D array (square matrix) | transpose then reverse rows, or rotate layer by layer | `nested loops with index algebra; swap elements in place` | In-place rotation uses O(1) extra space by transforming indices and swapping. Allocating a new matrix would use O(n^2) space. |
| LeetCode 54 Spiral Matrix | 2D array | traverse in layers: top row, right column, bottom row, left column | `four boundaries (top, bottom, left, right) updated after each side` | Tracking boundaries and spiraling inward visits each element exactly once in O(n*m) with O(1) extra space. |

## Claims and their checks

- `sliding-window-avoids-nesting`: Sliding window processes each element at most twice, keeping subarray problems O(n) instead of O(n^2).
- `prefix-sum-enables-constant-range-queries`: A prefix sum array answers any subarray-sum query in O(1) after O(n) preprocessing.
- `two-pointers-solve-ksum-in-polynomial`: Two pointers on a sorted array reduce k-sum from O(n^k) brute force to O(n^(k-1)) by solving one subproblem in linear time.
- `in-place-rotation-uses-constant-space`: Rotating a matrix 90 degrees in place uses O(1) extra space; allocating a new matrix uses O(n^2).
- `product-except-self-without-division`: Computing product of array except self is possible without division by combining left and right products.
