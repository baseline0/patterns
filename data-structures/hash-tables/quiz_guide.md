# Quiz: Hash tables: dict and set

> Generated from `content/`.

## 1. Why can a tuple be a dict key but a list cannot?

A. Tuples are faster to hash
B. A tuple is immutable, so its hash cannot change; a list is mutable and not hashable
C. Lists are too large to store
D. Dicts only accept strings and tuples

**Answer: B.** A key's hash must stay fixed while the key is stored. Only immutable values can guarantee that.

## 2. On average, what does membership testing cost in a set of n items?

A. O(1)
B. O(log n)
C. O(n)
D. O(n log n)

**Answer: A.** The hash picks a slot directly. Only collisions add probes, and those are rare.

## 3. Since Python 3.7, what does iterating over a dict return?

A. Keys in sorted order
B. Keys in insertion order
C. Keys in random order
D. Keys in order of their hash

**Answer: B.** Insertion order is a language guarantee, because entries are stored in a dense array in that order.

## 4. Why is the 'group anagrams' problem a fit for defaultdict(list)?

A. It sorts the words automatically
B. Each new key gets an empty list on first use, so grouping needs no existence check
C. It removes duplicate words
D. It keeps the groups sorted

**Answer: B.** defaultdict creates the missing list on access, so each word appends to its group in one step.
