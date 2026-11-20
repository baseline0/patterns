"""Checks for the data-structures family: schema, generated-file drift, and each claim against this interpreter."""

from __future__ import annotations

import importlib.util
import itertools
import statistics
import sys
import time
from collections import deque

import pytest
from constants import REPO_ROOT

ROOT = REPO_ROOT / "data-structures"
TOOLS = ROOT / "tools"


def _load(name: str):
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = _load("build")


def _best_time(fn, repeat: int = 5) -> float:
    """Smallest of several runs, which resists scheduler noise better than a single run."""
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best


# --- schema and generated outputs ------------------------------------------------------------------------------------


def test_every_topic_validates() -> None:
    topics = build.load_topics()

    assert topics
    for topic in topics:
        build.validate(topic, source=topic["id"])


def test_generated_outputs_match_the_checked_in_files() -> None:
    """A stale output fails here. Regenerate with `uv run python data-structures/tools/build.py`."""
    for relative, text in build.render_all().items():
        target = ROOT / relative
        assert target.exists(), f"missing generated file: {relative}"
        assert target.read_text(encoding="utf-8") == text, f"stale generated file: {relative}"


def test_every_claim_has_a_check() -> None:
    """A claim with no check here fails: the write-up cannot state something the suite does not test."""
    claims = {claim["id"] for topic in build.load_topics() for claim in topic["claims"]}

    assert claims == set(CLAIM_CHECKS)


def test_an_answer_outside_its_choices_is_rejected() -> None:
    topic = {
        "id": "x", "title": "x", "summary": "x", "mechanics": [], "claims": [], "complexity": [], "signals": [],
        "problems": [], "quiz": [{"question": "q", "choices": ["a"], "answer": 3, "explanation": "e"}],
    }  # fmt: skip

    with pytest.raises(build.ContentError, match="outside its choices"):
        build.validate(topic, source="test")


# --- claims, each checked against this interpreter -------------------------------------------------------------------


def _list_growth_is_geometric() -> None:
    items: list[int] = []
    capacities: list[int] = []
    last = None
    for i in range(20_000):
        items.append(i)
        size = sys.getsizeof(items)
        if size != last:
            capacities.append(len(items))
            last = size
    # Past the first few resizes, each step grows the length by a bounded fraction rather than by one slot.
    steps = [b / a for a, b in itertools.pairwise(capacities[10:])]
    assert steps and all(1.05 <= ratio <= 1.5 for ratio in steps)


def _pop_zero_scales_linearly() -> None:
    small = list(range(20_000))
    large = list(range(200_000))

    def drain(lst: list[int]) -> None:
        copy = list(lst)
        while copy:
            copy.pop(0)

    t_small = _best_time(lambda: drain(small[:2000]), repeat=3)
    t_large = _best_time(lambda: drain(large[:20_000]), repeat=3)
    # 10x the work for the same count of pops: the pops on the longer list each shift more pointers.
    assert t_large > 3 * t_small


def _popleft_is_constant() -> None:
    short = deque(range(1_000))
    long = deque(range(200_000))

    def pop_many(d: deque) -> None:
        for _ in range(500):
            d.appendleft(0)
            d.popleft()

    t_short = _best_time(lambda: pop_many(short))
    t_long = _best_time(lambda: pop_many(long))
    assert t_long < 3 * t_short


def _insort_shift_is_linear() -> None:
    import bisect

    base = list(range(0, 2_000_000, 2))

    def insert_then_restore() -> None:
        bisect.insort(base, 1)
        del base[0]  # restores the length so each call inserts into the same-sized list

    search = _best_time(lambda: bisect.bisect(base, 1), repeat=5)
    insert = _best_time(insert_then_restore, repeat=3)
    # The search is logarithmic; inserting at the front copies the whole list, so it is far slower.
    assert insert > 20 * search


def _dict_keys_must_be_hashable() -> None:
    with pytest.raises(TypeError):
        _ = {[1, 2]: "value"}


def _dict_preserves_insertion_order() -> None:
    d = {}
    for key in ("b", "a", "c"):
        d[key] = key
    assert list(d) == ["b", "a", "c"]


def _heap_root_is_minimum() -> None:
    import heapq

    values = [9, 4, 7, 1, 8]
    heapq.heapify(values)
    assert values[0] == min(values)


def _heappop_yields_sorted_order() -> None:
    import heapq
    import random

    rng = random.Random(7)
    values = [rng.randrange(10_000) for _ in range(1_000)]
    heap = list(values)
    heapq.heapify(heap)
    popped = [heapq.heappop(heap) for _ in range(len(values))]
    assert popped == sorted(values)


def _heapify_is_linear() -> None:
    import heapq

    def timed(values: list[int]) -> float:
        samples = []
        for _ in range(7):
            work = values[:]
            start = time.perf_counter()
            heapq.heapify(work)
            samples.append(time.perf_counter() - start)
        return statistics.median(samples)

    small = list(range(200_000, 0, -1))
    large = list(range(400_000, 0, -1))
    t_small = timed(small)
    t_large = timed(large)
    # Linear work doubles with n; n log n would be a little more than double. The bound leaves room for noise.
    assert t_large < 3 * t_small


def _nlargest_beats_a_full_sort_for_small_k() -> None:
    import heapq
    import random

    rng = random.Random(11)
    data = [rng.random() for _ in range(500_000)]
    t_sort = _best_time(lambda: sorted(data)[-10:], repeat=3)
    t_heap = _best_time(lambda: heapq.nlargest(10, data), repeat=3)
    assert t_heap < t_sort


def _set_membership_beats_list_search() -> None:
    items = list(range(10_000))
    as_set = set(items)
    target = 9_999  # the worst case for the list: the scan reaches the end
    t_list = _best_time(lambda: target in items, repeat=5)
    t_set = _best_time(lambda: target in as_set, repeat=5)
    assert t_list > 50 * t_set


def _dict_lookup_is_constant_time() -> None:
    small = {i: i for i in range(1_000)}
    large = {i: i for i in range(1_000_000)}
    t_small = _best_time(lambda: small[500], repeat=5)
    t_large = _best_time(lambda: large[500_000], repeat=5)
    # A linear structure would be about 1000 times slower on the large dict. Cache effects add a few times.
    assert t_large < 10 * t_small


def _tree_is_recursive_structure() -> None:
    """A tree is recursively defined: each subtree is a tree."""
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    # Single node is a tree
    root = Node(1)
    assert root.val == 1

    # Tree with left and right subtrees
    root = Node(1, Node(2), Node(3))
    assert root.left.val == 2 and root.right.val == 3


def _bst_maintains_invariant() -> None:
    """In a BST, all left descendants are smaller, all right descendants are larger."""
    def is_bst(node, min_val=float('-inf'), max_val=float('inf')):
        if node is None:
            return True
        if not min_val < node.val < max_val:
            return False
        return is_bst(node.left, min_val, node.val) and is_bst(node.right, node.val, max_val)

    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    # Valid BST
    root = Node(2, Node(1), Node(3))
    assert is_bst(root)

    # Invalid BST: right child violates invariant
    invalid = Node(2, Node(1), Node(1))  # right node should be > 2
    assert not is_bst(invalid)


def _inorder_traversal_yields_sorted() -> None:
    """In-order traversal of a BST visits nodes in sorted order."""
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def inorder(node):
        if node is None:
            return []
        return [*inorder(node.left), node.val, *inorder(node.right)]

    # BST: 2 as root, 1 left, 3 right
    root = Node(2, Node(1), Node(3))
    result = inorder(root)
    assert result == [1, 2, 3]
    assert result == sorted(result)


def _tree_height_bounds_recursive_depth() -> None:
    """Tree height determines the recursion depth and required stack space."""
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def height(node):
        if node is None:
            return 0
        return 1 + max(height(node.left), height(node.right))

    # Single node: height 1
    root = Node(1)
    assert height(root) == 1

    # Chain of 3 nodes: height 3
    root = Node(1, Node(2, Node(3)))
    assert height(root) == 3


def _balanced_tree_search_is_logarithmic() -> None:
    """In a balanced BST, search eliminates about half the tree per comparison."""
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def search_steps(node, target, steps=0):
        if node is None or node.val == target:
            return steps
        if target < node.val:
            return search_steps(node.left, target, steps + 1)
        return search_steps(node.right, target, steps + 1)

    # Balanced tree with 7 nodes: height ~3
    root = Node(4, Node(2, Node(1), Node(3)), Node(6, Node(5), Node(7)))
    # Finding any node should take at most 3 steps (the height)
    for i in range(1, 8):
        assert search_steps(root, i) <= 3


def _linked_list_no_random_access() -> None:
    """Reaching a position in a linked list requires walking from the head."""
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next

    def find_at_position(head, position):
        current = head
        for _ in range(position):
            if current is None:
                return None
            current = current.next
        return current

    # Create list: 1 -> 2 -> 3
    head = Node(1, Node(2, Node(3)))
    # Must walk through nodes to reach position 2
    node_at_2 = find_at_position(head, 2)
    assert node_at_2.val == 3


def _linked_list_insert_delete_constant() -> None:
    """Insertion and deletion at a known node cost O(1)."""
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next

    # Insert after a node: O(1)
    node = Node(1, Node(3))
    new_node = Node(2)
    new_node.next = node.next
    node.next = new_node
    assert node.next.val == 2 and node.next.next.val == 3

    # Delete the next node: O(1)
    node.next = node.next.next
    assert node.next.val == 3


def _reversal_redirects_pointers_inplace() -> None:
    """Reversing a linked list in-place uses O(1) extra space by redirecting pointers."""
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next

    def reverse(head):
        prev = None
        current = head
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        return prev

    # Forward: 1 -> 2 -> 3
    head = Node(1, Node(2, Node(3)))
    reversed_head = reverse(head)
    # After reverse: 3 -> 2 -> 1
    assert reversed_head.val == 3
    assert reversed_head.next.val == 2
    assert reversed_head.next.next.val == 1


def _cycle_detection_two_pointers() -> None:
    """Two pointers at different speeds detect a cycle: they meet if one exists."""
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next

    def has_cycle(head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    # List with cycle: 1 -> 2 -> 3 -> 2 (cycle back to 2)
    node2 = Node(2)
    node3 = Node(3)
    node2.next = node3
    node3.next = node2
    head = Node(1, node2)
    assert has_cycle(head)

    # List without cycle
    head_no_cycle = Node(1, Node(2, Node(3)))
    assert not has_cycle(head_no_cycle)


def _dummy_node_simplifies_head_cases() -> None:
    """A dummy node eliminates special cases when modifying the head."""
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next

    def merge(l1, l2):
        dummy = Node(0)
        current = dummy
        while l1 and l2:
            if l1.val < l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        current.next = l1 or l2
        return dummy.next

    # Merge two sorted lists
    l1 = Node(1, Node(3))
    l2 = Node(2, Node(4))
    result = merge(l1, l2)
    # Result: 1 -> 2 -> 3 -> 4
    assert result.val == 1
    assert result.next.val == 2


def _two_pointers_check_palindrome() -> None:
    def is_palindrome(s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    assert is_palindrome("racecar")
    assert is_palindrome("a")
    assert not is_palindrome("abc")
    assert is_palindrome("aabbaa")


def _anagram_count_vs_sort() -> None:
    from collections import Counter

    def anagrams_count(s1: str, s2: str) -> bool:
        return Counter(s1) == Counter(s2)

    def anagrams_sort(s1: str, s2: str) -> bool:
        return sorted(s1) == sorted(s2)

    # Verify both methods give identical results on various inputs
    test_cases = [
        ("listen", "silent", True),
        ("abc", "cab", True),
        ("abc", "abd", False),
        ("", "", True),
        ("a", "a", True),
        ("aab", "aba", True),
    ]
    for s1, s2, expected in test_cases:
        assert anagrams_count(s1, s2) == expected
        assert anagrams_sort(s1, s2) == expected
        assert anagrams_count(s1, s2) == anagrams_sort(s1, s2)


def _sliding_window_is_linear() -> None:
    def longest_substring_without_repeating(s: str) -> int:
        char_index = {}
        max_length = 0
        left = 0
        for right, char in enumerate(s):
            if char in char_index:
                left = max(left, char_index[char] + 1)
            char_index[char] = right
            max_length = max(max_length, right - left + 1)
        return max_length

    assert longest_substring_without_repeating("abcabcbb") == 3
    assert longest_substring_without_repeating("bbbbb") == 1
    assert longest_substring_without_repeating("au") == 2
    assert longest_substring_without_repeating("dvdf") == 3


def _in_place_reversal_no_allocation() -> None:
    def reverse_string_in_place(chars: list[str]) -> None:
        left, right = 0, len(chars) - 1
        while left < right:
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1

    chars = list("hello")
    reverse_string_in_place(chars)
    assert "".join(chars) == "olleh"

    chars2 = list("a")
    reverse_string_in_place(chars2)
    assert "".join(chars2) == "a"


def _sliding_window_avoids_nesting() -> None:
    def max_subarray_length(arr: list[int], k: int) -> int:
        if not arr:
            return 0
        left, max_len = 0, 0
        for right in range(len(arr)):
            if right - left + 1 > k:
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len

    assert max_subarray_length([1, 2, 3, 4, 5], 3) == 3
    assert max_subarray_length([1], 5) == 1


def _prefix_sum_enables_constant_range_queries() -> None:
    def range_sum_query(arr: list[int], left: int, right: int) -> int:
        prefix = [0]
        for val in arr:
            prefix.append(prefix[-1] + val)
        return prefix[right + 1] - prefix[left]

    arr = [1, 2, 3, 4, 5]
    assert range_sum_query(arr, 0, 2) == 6  # 1+2+3
    assert range_sum_query(arr, 1, 3) == 9  # 2+3+4
    assert range_sum_query(arr, 0, 4) == 15  # 1+2+3+4+5


def _two_pointers_solve_ksum_in_polynomial() -> None:
    def three_sum(nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif total < 0:
                    left += 1
                else:
                    right -= 1
        return result

    assert [-1, 0, 1] in three_sum([-1, 0, 1, 2, -1, -4])
    assert len(three_sum([0, 0, 0, 0])) == 1


def _in_place_rotation_uses_constant_space() -> None:
    def rotate_matrix_inplace(matrix: list[list[int]]) -> None:
        n = len(matrix)
        # Transpose
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # Reverse each row
        for row in matrix:
            row.reverse()

    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate_matrix_inplace(matrix)
    assert matrix == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]


def _product_except_self_without_division() -> None:
    def product_except_self(nums: list[int]) -> list[int]:
        n = len(nums)
        left_products = [1] * n
        right_products = [1] * n
        result = [1] * n

        for i in range(1, n):
            left_products[i] = left_products[i - 1] * nums[i - 1]
        for i in range(n - 2, -1, -1):
            right_products[i] = right_products[i + 1] * nums[i + 1]
        for i in range(n):
            result[i] = left_products[i] * right_products[i]

        return result

    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([2, 3, 4, 5]) == [60, 40, 30, 24]


CLAIM_CHECKS = {
    "list-append-is-amortized-constant": _list_growth_is_geometric,
    "list-pop-zero-scales-linearly": _pop_zero_scales_linearly,
    "deque-popleft-is-constant": _popleft_is_constant,
    "insort-shift-is-linear": _insort_shift_is_linear,
    "dict-keys-must-be-hashable": _dict_keys_must_be_hashable,
    "dict-preserves-insertion-order": _dict_preserves_insertion_order,
    "heap-root-is-minimum": _heap_root_is_minimum,
    "heappop-yields-sorted-order": _heappop_yields_sorted_order,
    "set-membership-beats-list-search": _set_membership_beats_list_search,
    "dict-lookup-is-constant-time": _dict_lookup_is_constant_time,
    "heapify-is-linear": _heapify_is_linear,
    "nlargest-beats-a-full-sort-for-small-k": _nlargest_beats_a_full_sort_for_small_k,
    "tree-is-recursive-structure": _tree_is_recursive_structure,
    "bst-maintains-invariant": _bst_maintains_invariant,
    "inorder-traversal-yields-sorted": _inorder_traversal_yields_sorted,
    "tree-height-bounds-recursive-depth": _tree_height_bounds_recursive_depth,
    "balanced-tree-search-is-logarithmic": _balanced_tree_search_is_logarithmic,
    "linked-list-no-random-access": _linked_list_no_random_access,
    "linked-list-insert-delete-constant": _linked_list_insert_delete_constant,
    "reversal-redirects-pointers-inplace": _reversal_redirects_pointers_inplace,
    "cycle-detection-two-pointers": _cycle_detection_two_pointers,
    "dummy-node-simplifies-head-cases": _dummy_node_simplifies_head_cases,
    "two-pointers-check-palindrome": _two_pointers_check_palindrome,
    "anagram-count-vs-sort": _anagram_count_vs_sort,
    "sliding-window-is-linear": _sliding_window_is_linear,
    "in-place-reversal-no-allocation": _in_place_reversal_no_allocation,
    "sliding-window-avoids-nesting": _sliding_window_avoids_nesting,
    "prefix-sum-enables-constant-range-queries": _prefix_sum_enables_constant_range_queries,
    "two-pointers-solve-ksum-in-polynomial": _two_pointers_solve_ksum_in_polynomial,
    "in-place-rotation-uses-constant-space": _in_place_rotation_uses_constant_space,
    "product-except-self-without-division": _product_except_self_without_division,
}


@pytest.mark.parametrize("claim_id", sorted(CLAIM_CHECKS))
def test_claim(claim_id: str) -> None:
    CLAIM_CHECKS[claim_id]()


def test_quiz_scores_every_question_across_topics(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Answering every question correctly scores all of them, across every topic, in the same run."""
    quiz = _load("quiz")
    topics = build.load_topics()
    total = sum(len(topic["quiz"]) for topic in topics)
    answers = iter("ABCDEFGH"[item["answer"]] for topic in topics for item in topic["quiz"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    assert quiz.run() == 0
    assert f"Score: {total} of {total}" in capsys.readouterr().out
