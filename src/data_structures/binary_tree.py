"""Implementation of a recursive binary tree structure with common methods."""
import reprlib

from collections.abc import Generator
from typing import Optional, Generic, TypeVar

# TODO: tests

T = TypeVar("T")


class BinaryTree(Generic[T]):
    """Recursively defined binary tree."""

    __slots__ = ("left", "right", "data")

    data: Optional[T]
    left: Optional["BinaryTree"]
    right: Optional["BinaryTree"]

    def __init__(self,
                 left: Optional["BinaryTree"] = None,
                 right: Optional["BinaryTree"] = None,
                 data: Optional[T] = None):
        self.left = left
        self.right = right
        self.data = data

    @reprlib.recursive_repr()
    def __repr__(self):
        repr_left = repr(self.left) if self.left is not None else ""
        repr_right = repr(self.right) if self.right is not None else ""
        repr_data = repr(self.data) if self.data is not None else ""
        return f"({repr_data}{repr_left}{repr_right})"

    def full_traversal(
            self) -> Generator[tuple["BinaryTree", int, int], None, None]:
        """Do a depth-first traversal of the tree, visiting each node thrice.

        Yields 3-tuples of the node being visited, the visit index, and the
        depth. The visits with index 0/1/2 form a pre/in/post-order traversal.
        """
        stack = [[self, 0]]
        while stack:
            node, visit = stack[-1]
            yield node, visit, len(stack) - 1

            if visit == 0:
                stack[-1][1] = 1
                if node.left is not None:
                    stack.append([node.left, 0])
            elif visit == 1:
                stack[-1][1] = 2
                if node.right is not None:
                    stack.append([node.right, 0])
            else:
                stack.pop()

    def preorder_traversal(self) -> Generator["BinaryTree", None, None]:
        popped = False
        stack = [self]
        while stack:
            if popped:
                node = stack.pop()
                if node.right is not None:
                    stack.append(node.right)
                    popped = False
            else:
                node = stack[-1]
                yield node
                if node.left is not None:
                    stack.append(node.left)
                else:
                    popped = True

    def inorder_traversal(self) -> Generator["BinaryTree", None, None]:
        popped = False
        stack = [self]
        while stack:
            if popped:
                node = stack.pop()
                yield node
                if node.right is not None:
                    stack.append(node.right)
                    popped = False
            else:
                node = stack[-1]
                if node.left is not None:
                    stack.append(node.left)
                else:
                    popped = True
