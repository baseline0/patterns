# Hash tables: dict and set

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

A dict and a set find an item by hashing its key, so a lookup costs about the same whether the container holds ten items or a million. The price is that keys must be hashable and must not change while they are stored.

## hash, then probe

Python computes a hash for each key and uses it to pick a starting slot. If that slot is taken by a different key, the table probes further slots. With a sensible fill level, the expected number of probes stays small, which is why lookup, insert, and delete are O(1) on average.

## a compact layout since 3.6

CPython keeps entries in a dense array in insertion order, and a separate sparse index maps hashes to positions in that array. The dense array is what keeps iteration in insertion order, and it uses less memory than a table of mostly empty slots.

## why keys must be hashable and stable

A key's hash decides where it is stored. If a key changes after it is stored, its hash changes, and the table looks in the wrong slot and cannot find it. That is why a list cannot be a key: it is mutable and not hashable. A tuple of immutable items can be a key.

## Complexity

| Operation | Time | Note |
| --- | --- | --- |
| `dict[key] / key in dict` | O(1) average | worst case O(n) when hashes collide; rare with a good hash |
| `dict[key] = value` | O(1) average | amortized, including the occasional resize |
| `set add / remove / in` | O(1) average | a dict with no values |
| `list membership (x in list)` | O(n) | for comparison: a linear scan |

## Signal to structure

| Signal in the problem | Requirement | Structure | Python tool | Example |
| --- | --- | --- | --- | --- |
| Has this value been seen before, in one pass | O(1) per check | hash set | `set` | Two Sum (LeetCode 1): a dict of values already seen |
| Group items that share a computed key | O(1) per item to find its group | hash table of lists | `collections.defaultdict(list)` | Group Anagrams (LeetCode 49) |
| Find the longest run of consecutive values without sorting | O(n) total, each value checked in O(1) | hash set | `set` | Longest Consecutive Sequence (LeetCode 128) |

## Problems mapped to this topic

| Problem | Container | Pattern | Python tool | Why |
| --- | --- | --- | --- | --- |
| LeetCode 1 Two Sum | hash table (dict) | complement lookup | `dict: store each value's index, check for the complement` | Looking up target minus the current value is O(1), so one pass finds the pair. |
| LeetCode 49 Group Anagrams | hash table of lists | group by a canonical key | `collections.defaultdict(list), keyed by the sorted letters` | Anagrams share a key, so each word joins its group with one lookup. |
| LeetCode 128 Longest Consecutive Sequence | hash set | start only at the beginning of a run | `set: membership checks` | Checking a value's neighbours is O(1), and only run starts need extending, so the total stays O(n). |

## Claims and their checks

- `dict-keys-must-be-hashable`: A dict key must be hashable. A list is not hashable, so it cannot be a key.
- `dict-preserves-insertion-order`: dict iteration follows insertion order (a language guarantee since Python 3.7).
- `set-membership-beats-list-search`: Testing membership in a set is far faster than a linear search of a list of the same items.
- `dict-lookup-is-constant-time`: A dict lookup does not grow with the dict: a dict 1000 times larger costs far less than 1000 times more per lookup.
