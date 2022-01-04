"""Exact and approximate algorithms for vertex coloring."""

from typing import TypeAlias, Optional
from collections.abc import Iterable

AdjacencyList: TypeAlias = list[list[int]]


def color_greedy(adj: AdjacencyList,
                 order: Optional[Iterable[int]] = None) -> list[int]:
    """Return a greedy coloring of the vertices.

    Uses at most D + 1 colors, where D is the maximum vertex degree.

    If order is given, it must be an iterable containing each vertex once.

    Complexity: O(n + m)
    """
    n = len(adj)
    colors = [-1 for _ in range(n)]

    if order is None:
        order = range(n)

    for u in order:
        neighbor_colors = set(colors[v] for v in adj[u])
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[u] = color

    return colors
