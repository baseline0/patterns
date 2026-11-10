# Quiz: Arrays and 2D arrays: subarrays, sliding window, and in-place operations

> Generated from `content/`.

## 1. In a sliding window for 'longest substring without repetition,' what does moving the left pointer accomplish?

A. Adds a new character to the window
B. Removes a character from the window to eliminate a repetition
C. Resets the window to start over
D. Moves to the center of the string

**Answer: B.** When a repeated character is found, the left pointer contracts to exclude the older occurrence and maintain the no-repeat property.

## 2. A prefix sum array allows answering 'sum of elements from index i to j' in what time?

A. O(n)
B. O(j - i)
C. O(1)
D. O(log n)

**Answer: C.** Prefix[j] - prefix[i-1] is a single array lookup. Preprocessing takes O(n); each query is O(1).

## 3. In 3Sum, after sorting the array, why do we use two pointers instead of nested loops?

A. Two pointers are always faster than nested loops in general
B. Two pointers reduce the inner loop from O(n) to O(1), making 3Sum O(n^2) instead of O(n^3)
C. Nested loops are not allowed on sorted arrays
D. Two pointers find the exact center of the array

**Answer: B.** Fixing one element and using two pointers to find the complementary pair is O(n) per element, so O(n^2) total with sorting.

## 4. Why can product of array except self be computed without division?

A. Division would lose precision for floating-point numbers
B. Left and right products multiply to give the product of all except element i
C. All elements are guaranteed to be non-zero
D. Multiplication is always faster than division

**Answer: B.** Prefix products (left of i) and suffix products (right of i) are computed separately, then combined. This avoids division by zero and is general.

## 5. What is the space complexity of rotating a 90-degree matrix in place using transpose and row reversal?

A. O(n)
B. O(n^2)
C. O(1)
D. O(log n)

**Answer: C.** In-place rotation using transpose and row reversal (or layer-by-layer swaps) uses only a constant number of temporary variables.
