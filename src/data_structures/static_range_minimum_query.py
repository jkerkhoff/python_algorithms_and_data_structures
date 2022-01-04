"""Implementation of a constant time query, linear space RMQ data structure.

Mostly based on presentation in the following MIT OCW lecture:
https://www.youtube.com/watch?v=0rCFkuQS968
(MIT 6.851 Advanced Data Structures, Spring 2012, Erik Demaine)

I believe that lecture in turn is based on this paper:
https://www.ics.uci.edu/~eppstein/261/BenFar-LCA-00.pdf

My implementation differs slightly in that I use a sparse table data structure
for the individual blocks. While this doesn't change the asymptotic complexity,
it reduces construction time quite significantly in practice, though probably
at the cost of somewhat slower (but still constant time) queries.

Unfortunately (?) my implementation appears to be outperformed by a simple
sparse table approach on all input sizes I have managed to test.
"""

import math
import operator
from typing import TypeVar, Generic
from collections.abc import Iterable

from src.data_structures.cartesian_tree import build_cartesian_index_tree

# TODO: clean up and optimize implementation, document

T = TypeVar("T", int, float)


class StaticRMQLogTable:
    """O(n lg n) build/space, O(1) query sparse table RMQ data structure."""

    __slots__ = ("_table", "_values")

    _table: list[list[int]]
    _values: list[int]

    def __init__(self, values: list[int]):
        table = [[]]
        n = len(values)
        for i in range(n - 1):
            if values[i] <= values[i + 1]:
                table[-1].append(i)
            else:
                table[-1].append(i + 1)

        k = 2
        while k < n:
            table.append([])
            for left in range(n - k):
                idx_lo = table[-2][left]
                idx_hi = table[-2][left + k // 2]
                if values[idx_lo] <= values[idx_hi]:
                    table[-1].append(idx_lo)
                else:
                    table[-1].append(idx_hi)
            k *= 2

        self._table = table
        self._values = values

    def idx_query(self, start: int, stop: int):
        """Return the index of the smallest element in the given range.

        If there are multiple, return the one with the lowest index.
        """
        if stop == -1:
            stop = len(self._values) - 1

        if start == stop:
            return start

        exponent = int(math.log2(stop - start))
        idx_lo = self._table[exponent][start]
        idx_hi = self._table[exponent][stop - (1 << exponent)]
        if self._values[idx_lo] <= self._values[idx_hi]:
            return idx_lo
        else:
            return idx_hi


class StaticRMQ(Generic[T]):
    """O(n) build/space, O(1) query RMQ data structure."""

    __slots__ = ("_block_size", "_euler_indices", "_euler_values",
                 "_summary_indices", "_summary_table", "_block_tables",
                 "_euler_first_encounters")

    _block_size: int
    _euler_indices: list[int]
    _euler_values: list[T]
    _summary_indices: list[int]
    _summary_table: StaticRMQLogTable
    _block_tables: list[StaticRMQLogTable]
    _euler_first_encounters: list[int]

    def __init__(self, iterable: Iterable[T]):
        # Euler tour stuff
        values = list(iterable)
        tree = build_cartesian_index_tree(values)
        euler_indices = []
        euler_values = []
        euler_depths = []
        euler_first_encounters = [-1 for _ in range(len(values))]
        for node, _, depth in tree.full_traversal():
            if euler_first_encounters[node.data] == -1:
                euler_first_encounters[node.data] = len(euler_indices)
            if not euler_indices or euler_indices[-1] != node.data:
                euler_indices.append(node.data)
                euler_values.append(values[node.data])
                euler_depths.append(depth)

        n = len(euler_indices)
        block_size = max(1, int(math.log2(n) / 2))

        # summary layer minima
        summary_indices = []
        summary_values = []
        for start in range(0, n, block_size):
            min_idx, min_val = min(enumerate(euler_depths[start:start +
                                                          block_size]),
                                   key=operator.itemgetter(1))
            summary_indices.append(start + min_idx)
            summary_values.append(min_val)

        # summary layer log lookup table
        summary_table = StaticRMQLogTable(summary_values)

        # lookup tables
        def pmin_seq_type(seq: list[int]) -> int:
            sequence_type = 0
            multiplier = 1
            for i in range(len(seq) - 1):
                sequence_type += multiplier * (seq[i + 1] - seq[i] + 1) // 2
                multiplier *= 2
            return sequence_type

        block_tables = []
        type_table_map = {}
        for start in range(0, n, block_size):
            seq_type = pmin_seq_type(euler_depths[start:start + block_size])
            if seq_type not in type_table_map:
                seq_table = StaticRMQLogTable(euler_depths[start:start +
                                                           block_size])
                type_table_map[seq_type] = seq_table
            block_tables.append(type_table_map[seq_type])

        self._block_size = block_size
        self._euler_indices = euler_indices
        self._euler_values = euler_values
        self._summary_indices = summary_indices
        self._summary_table = summary_table
        self._block_tables = block_tables
        self._euler_first_encounters = euler_first_encounters

    def idx_query(self, start: int, stop: int):  # stop included in bound
        # map bounds into euler tour
        start = self._euler_first_encounters[start]
        stop = self._euler_first_encounters[stop]
        if start > stop:
            start, stop = stop, start

        block_left = start // self._block_size
        block_right = stop // self._block_size

        if block_left == block_right:
            # entire lookup is in one block, so logic is a bit different
            left = start - block_left * self._block_size
            right = stop - block_left * self._block_size
            idx_in_block = self._block_tables[block_left].idx_query(
                left, right)
            idx_in_euler = block_left * self._block_size + idx_in_block
            return self._euler_indices[idx_in_euler]

        # left endpoint lookup
        left_left = start - block_left * self._block_size
        left_idx = self._block_tables[block_left].idx_query(left_left, -1)
        left_idx += block_left * self._block_size
        ans_idx = left_idx

        if block_right - block_left > 1:
            summary_idx = self._summary_table.idx_query(
                block_left + 1, block_right - 1)
            summary_idx = self._summary_indices[summary_idx]
            if self._euler_values[summary_idx] < self._euler_values[ans_idx]:
                ans_idx = summary_idx

        # right endpoint lookup
        right_right = stop - block_right * self._block_size
        right_idx = self._block_tables[block_right].idx_query(0, right_right)
        right_idx += block_right * self._block_size

        if self._euler_values[right_idx] < self._euler_values[ans_idx]:
            ans_idx = right_idx

        return self._euler_indices[ans_idx]
