"""Implementation of a linear time Cartesian tree algorithm.

Implemented from memory after watching the following MIT OCW lecture:
https://www.youtube.com/watch?v=0rCFkuQS968
(MIT 6.851 Advanced Data Structures, Spring 2012, Erik Demaine)

And reading part of the following Wikipedia article:
https://en.wikipedia.org/wiki/Cartesian_tree
"""

import operator
from collections.abc import Callable, Sequence
from typing import Optional, TypeVar

from src.data_structures.binary_tree import BinaryTree

T = TypeVar("T", int, float)

Comp = Callable[[T, T], bool]


def build_cartesian_index_tree(values: Sequence[T],
                               comp: Optional[Comp] = None) -> BinaryTree[int]:
    """
    Construct a Cartesian tree from a sequence, storing indices in the nodes.

    Each node in the tree corresponds to (and stores) an index into the input
    sequence. It is a min-heap w.r.t. the corresponding values, and an in-order
    traversal returns the indices in increasing order.

    If comp is not None it must induce a complete order, and will be used to
    compare values. By default the built-in less-than operator is used.

    Complexity: O(len(values))
    """
    if comp is None:
        comp = operator.lt

    if not values:
        raise ValueError(
            "Failed to build cartesian tree: empty input sequence")

    root = BinaryTree(data=0)
    stack = [root]
    for idx in range(1, len(values)):
        new_node = BinaryTree(data=idx)

        if comp(values[idx], values[stack[-1].data]):
            while stack and comp(values[idx], values[stack[-1].data]):
                stack.pop()

            if stack:
                new_node.left = stack[-1].right
                stack[-1].right = new_node
            else:
                new_node.left = root
                root = new_node
        else:
            stack[-1].right = new_node

        stack.append(new_node)

    return root
