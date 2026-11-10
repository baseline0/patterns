# Quiz: Strings: pattern matching, substring search, and palindromes

> Generated from `content/`.

## 1. When two pointers check a palindrome from the ends inward, what triggers a failed check?

A. The left pointer reaches the right pointer
B. Characters at the current positions do not match
C. The string has an odd length
D. The string contains a space

**Answer: B.** Palindromes have matching characters at symmetric positions. Any mismatch means the string is not a palindrome.

## 2. Why is checking if two strings are anagrams using Counter faster than sorting both?

A. Counter is implemented in C and always faster
B. Counter is O(n); sorting both is O(n log n)
C. Counter eliminates duplicate characters
D. Sorting cannot compare frequencies

**Answer: B.** Counting characters is linear. Sorting is O(n log n), so dict lookup is more efficient for anagram detection.

## 3. In the sliding-window approach to 'longest substring without repetition,' what does the left pointer do?

A. Tracks the start of the current valid substring
B. Points to the rightmost character
C. Remains at the first character
D. Skips whitespace

**Answer: A.** The right pointer expands the window; the left retracts when a repeat is found. The distance between them is the substring length.

## 4. Why does reversing a string with two pointers and swapping use O(1) space while str[::-1] uses O(n)?

A. Swapping modifies the original; slicing allocates a new string
B. Two pointers are inherently more efficient
C. Slicing only works on immutable strings
D. Swapping runs in the CPU cache

**Answer: A.** Strings in Python are immutable, so str[::-1] allocates a new string. In-place swaps work on lists or character arrays.

## 5. When comparing anagrams, why must we count all characters instead of just checking for duplicates?

A. Duplicates are not relevant to anagrams
B. We need to verify the same multiset of characters appears in both strings
C. Counting is always faster than checking
D. Anagrams only have unique characters

**Answer: B.** Anagrams have the same characters with the same frequencies. Checking duplicates alone misses frequency differences.
