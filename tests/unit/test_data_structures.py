"""Checks for the data-structures family: schema, generated-file drift, and each claim against this interpreter."""

from __future__ import annotations

import importlib.util
import itertools
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

    small = list(range(200_000, 0, -1))
    large = list(range(400_000, 0, -1))
    t_small = _best_time(lambda: heapq.heapify(small[:]), repeat=5)
    t_large = _best_time(lambda: heapq.heapify(large[:]), repeat=5)
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


CLAIM_CHECKS = {
    "list-append-is-amortized-constant": _list_growth_is_geometric,
    "list-pop-zero-scales-linearly": _pop_zero_scales_linearly,
    "deque-popleft-is-constant": _popleft_is_constant,
    "insort-shift-is-linear": _insort_shift_is_linear,
    "dict-keys-must-be-hashable": _dict_keys_must_be_hashable,
    "dict-preserves-insertion-order": _dict_preserves_insertion_order,
    "heap-root-is-minimum": _heap_root_is_minimum,
    "heappop-yields-sorted-order": _heappop_yields_sorted_order,
    "heapify-is-linear": _heapify_is_linear,
    "nlargest-beats-a-full-sort-for-small-k": _nlargest_beats_a_full_sort_for_small_k,
}


@pytest.mark.parametrize("claim_id", sorted(CLAIM_CHECKS))
def test_claim(claim_id: str) -> None:
    CLAIM_CHECKS[claim_id]()
