import functools
import heapq
import itertools

from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, initialize, rule, invariant, precondition

from src.data_structures.priority_queue import PriorityQueue, Heap, VEBQueue


@functools.total_ordering
class HeapQNode:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other: "HeapQNode"):
        return self.key == other.key

    def __lt__(self, other: "HeapQNode"):
        return self.key < other.key


# TODO: figure out a clean way to constrain keys only for VEB
KEYS = st.integers(0, 2**64 - 1)
VALS = st.integers()


class PriorityQueueTester(RuleBasedStateMachine):
    IMPL = PriorityQueue

    queue: PriorityQueue | None
    heap: list[HeapQNode]

    def __init__(self):
        super().__init__()
        self.queue = None
        self.heap = []

    @initialize(iterable=st.iterables(st.tuples(KEYS, VALS)))
    def init(self, iterable):
        it1, it2 = itertools.tee(iterable)
        self.queue = self.IMPL(it1)
        self.heap = [HeapQNode(k, v) for k, v in it2]
        heapq.heapify(self.heap)

    @rule()
    def top(self):
        if self.heap:
            k, v = self.queue.top()
            assert k == self.heap[0].key
        else:
            assert self.queue.top() is None

    @rule(key=KEYS, value=VALS)
    def push(self, key, value):  # TODO: test correct values
        self.queue.push(key, value)
        heapq.heappush(self.heap, HeapQNode(key, value))

    @precondition(lambda self: bool(self.heap))
    @rule()
    def pop(self):
        qk, qv = self.queue.pop()
        node = heapq.heappop(self.heap)
        assert qk == node.key

    @precondition(lambda self: bool(self.heap))
    @rule(key=KEYS, value=VALS)
    def pop_push(self, key, value):
        qk, qv = self.queue.pop_push(key, value)
        node = heapq.heapreplace(self.heap, HeapQNode(key, value))
        assert qk == node.key

    @rule(key=KEYS, value=VALS)
    def push_pop(self, key, value):
        qk, qv = self.queue.push_pop(key, value)
        node = heapq.heappushpop(self.heap, HeapQNode(key, value))
        assert qk == node.key

    @invariant()
    def bool(self):
        assert bool(self.queue) == bool(self.heap)

    @invariant()
    def len(self):
        assert len(self.queue) == len(self.heap)


class HeapTester(PriorityQueueTester):
    IMPL = Heap


TestHeapStateful = HeapTester.TestCase


class VEBQueueTester(PriorityQueueTester):
    IMPL = VEBQueue


TestVEBQueueStateful = VEBQueueTester.TestCase
