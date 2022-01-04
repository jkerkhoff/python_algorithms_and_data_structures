"""Implementation of the union find/disjoint set forest data structure.

Implemented from memory, but most likely based on Wikipedia's presentation:
https://en.wikipedia.org/wiki/Disjoint-set_data_structure

Current implementation uses union by rank with path halving.
"""

# TODO: maybe use array for ranks, since the values are at most logarithmic


class UnionFind:
    """Data structure for keeping track of/merging subsets of a partition."""

    __slots__ = ('_parents', '_ranks')

    _parents: list[int]
    _ranks: list[int]

    def __init__(self, size: int):
        """Initialize a partition with size singleton sets.

        Complexity: O(size)
        """
        self._parents = list(range(size))
        self._ranks = [0 for _ in range(size)]

    def make_set(self) -> int:
        """Create a new singleton set and return its index.

        Complexity: O(1)
        """
        x = len(self._parents)
        self._parents.append(x)
        self._ranks.append(0)
        return x

    def find(self, x: int) -> int:
        """Find the current representative of the set containing x.

        Note that while the representatives of two elements of the same set are
        always equal, the representative of a set can change over time.

        Complexity: O(iAck(size)) amortized
        """
        while x != self._parents[x]:
            # path halving
            x, self._parents[x] = self._parents[x], self._parents[
                self._parents[x]]
        return x

    def merge(self, x: int, y: int) -> bool:
        """Merge the set containing x with the set containing y.

        If x and y were originally in different sets, return True.
        Otherwise, return False.

        Complexity: O(iAck(size)) amortized
        """
        x = self.find(x)
        y = self.find(y)

        if x != y:
            # union by rank
            if self._ranks[x] > self._ranks[y]:
                x, y = y, x

            if self._ranks[x] == self._ranks[y]:
                self._ranks[y] += 1

            self._parents[x] = y
            return True
        return False

    def __len__(self) -> int:
        return len(self._parents)
