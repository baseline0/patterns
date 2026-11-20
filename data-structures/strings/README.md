# Strings: pattern matching, substring search, and palindromes

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

- Explore in local catalogue: `just -f site/justfile serve` → `site/index.html`

Strings are sequences of characters. Finding patterns in strings uses two pointers to check palindromes and reverse sequences without allocating new strings. Hashing character positions or frequencies enables substring search and anagram detection in linear time without nested loops.

## two pointers for symmetry checks

Two pointers starting from opposite ends move inward simultaneously. This checks palindromes and validates symmetric properties without reversing the string. The only extra space is the pointers.

## character frequency hashing

A dict or Counter maps characters to their counts or positions. Anagrams share the same character counts, and comparing counts is O(1) per character instead of O(n log n) if the strings were sorted.

## sliding window for unique-character substrings

One pointer extends a window to add characters; the other retracts when a condition is violated (repetition, invalid character). Each character is added and removed once, keeping work linear.

## pattern searching and string reversal

Reversing words or characters in place uses index swapping. Finding a substring uses either naive position-by-position comparison or a rolling hash to detect the pattern in O(n).

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `palindrome check (two pointers)` | O(n) time, O(1) space | move from ends inward; no allocation |
| `reverse string in place (swap)` | O(n) time, O(1) space | swap characters with two pointers |
| `anagram check (character count)` | O(n) | dict lookups are O(1); faster than sorting |
| `anagram check (sort both)` | O(n log n) | for comparison; sorting is more overhead than needed |
| `substring search (naive)` | O(n*m) | nested loop: for each position, match up to m chars |
| `longest substring without repeats` | O(n) | sliding window; each char seen at most twice |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Verify a string reads the same forward and backward | O(n) time, O(1) space | two pointers from ends | `str indexing` | Valid Palindrome (LeetCode 125) |
| Compare words by their letters, ignoring order | O(n) without sorting | character frequency dict | `collections.Counter` | Valid Anagram (LeetCode 242) |
| Find longest substring with a property (no repeats, all vowels, etc.) | O(n) in one pass | sliding window with dict | `dict or set to track character presence` | Longest Substring Without Repeating Characters (LeetCode 3) |
| Locate first occurrence of a pattern or substring | O(n) or O(n+m) without O(n*m) | rolling hash or KMP | `str.find or manual index-by-index` | Implement strStr (LeetCode 28) |
| Reverse, rotate, or rearrange words in a string | O(n) time, O(1) space | two-pointer reversal | `str.split and join, or manual swap` | Reverse Words in a String (LeetCode 151) |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| LeetCode 28 Implement strStr | string | substring search at each position | `str.find or manual char-by-char comparison` | Comparing characters position by position finds the first match in O(n*m). Rolling hash improves to O(n) but naive is sufficient for moderate lengths. |
| LeetCode 125 Valid Palindrome | string | two pointers ignoring non-alphanumeric | `str.isalnum and lower for filtering; two pointers` | Two pointers from the ends check symmetry in O(n) without allocating a reversed or cleaned string. |
| LeetCode 242 Valid Anagram | character frequency dict | count and compare | `collections.Counter` | Counting character frequencies is O(n). Sorting both strings is O(n log n). Counter is optimal for this check. |
| LeetCode 58 Length of Last Word | string | reverse scan to skip trailing spaces | `str.split or manual indexing from the end` | Scanning backward from the end finds the last word in one pass, avoiding the overhead of splitting and reversing. |
| LeetCode 151 Reverse Words in a String | string | word-by-word reversal with space handling | `str.split and reverse and join, or two-pointer character swap` | Using split().reverse().join() is Pythonic and concise. Manual reversal in place avoids intermediate allocations. |
| LeetCode 680 Valid Palindrome II | string | two pointers with one skip allowed | `two-pointer recursion or backtracking to check both skip cases` | When a mismatch is found, we must try skipping the left or right character. Backtracking checks both without full string duplication. |

## Claims and their checks

- `two-pointers-check-palindrome`: Two pointers from opposite ends can check a palindrome in O(n) time and O(1) space without reversing.
- `anagram-count-vs-sort`: Anagrams have identical character counts. Comparing counts is O(n); sorting both strings is O(n log n).
- `sliding-window-is-linear`: A sliding window processes each character at most twice, keeping substring search O(n) instead of O(n^2).
- `in-place-reversal-no-allocation`: Reversing a string in place by swapping characters uses O(1) space; building a reversed copy uses O(n).
