"""A collection of algorithms for constructing minimum spanning forests for edge-weighted undirected graphs."""

import heapq
from typing import TypeVar
from collections.abc import Iterable

from src.data_structures.union_find import UnionFind

Weight = TypeVar("Weight", float, int)
Edge = tuple[int, int, Weight]


def kruskal(n: int, edges: Iterable[Edge]) -> list[Edge]:
    """Compute a minimum spanning forest using Kruskal's algorithm.

    Complexity: O(E lg E) = O(E lg V)
    """
    components = UnionFind(n)
    queue = [(weight, u, v) for u, v, weight in edges]
    heapq.heapify(queue)

    result = []
    while queue and len(result) < n - 1:
        weight, u, v = heapq.heappop(queue)

        if components.find(u) != components.find(v):
            components.merge(u, v)
            result.append((u, v, weight))

    return result


def prim(n: int, edges: Iterable[Edge]) -> list[Edge]:
    """Compute a minimum spanning forest using Prim's algorithm.

    Complexity: O(E lg E) = O(E lg V)
    """
    adj = [[] for _ in range(n)]
    for u, v, weight in edges:
        adj[u].append((v, weight))
        adj[v].append((u, weight))

    cheapest_edge = [None for _ in range(n)]
    in_forest = [False for _ in range(n)]
    forest_vertices = 0

    result = []
    for root in range(n):
        if in_forest[root]:
            continue

        in_forest[root] = True
        forest_vertices += 1

        if forest_vertices == n:
            return result

        queue = []

        for v, weight in adj[root]:
            if cheapest_edge[v] is None or cheapest_edge[v][1] < weight:
                cheapest_edge[v] = (root, weight)
                heapq.heappush(queue, (weight, v))

        while queue:
            weight, u = heapq.heappop(queue)
            if not in_forest[u]:
                in_forest[u] = True
                forest_vertices += 1

                v, weight = cheapest_edge[u]
                result.append((u, v, weight))  # TODO: input order

                if forest_vertices == n:
                    return result

                for v, weight in adj[u]:
                    if not in_forest[v] and (cheapest_edge[v] is None
                                             or cheapest_edge[v][1] < weight):
                        cheapest_edge[v] = (u, weight)
                        heapq.heappush(queue, (weight, v))


def boruvka(n: int, edges: Iterable[Edge]) -> list[Edge]:
    """Compute a minimum spanning forest using Borůvka's algorithm.

    Complexity: O(E lg V)
    """
    pass  # TODO


def chazelle(n: int, edges: Iterable[Edge]) -> list[Edge]:
    """Compute a minimum spanning forest using Chazelle's algorithm.

    Complexity: O(E iack(E, V))
    """
    pass  # TODO


def karger_klein_tarjan(n: int, edges: Iterable[Edge]) -> list[Edge]:
    """Compute a minimum spanning forest using KKT's randomized algorithm.

    Complexity: O(E) expected
    """
    pass  # TODO
