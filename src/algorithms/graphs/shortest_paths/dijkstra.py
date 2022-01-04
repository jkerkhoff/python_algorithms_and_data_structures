"""Implementations of variations of Dijkstra's algorithm."""
import heapq
from dataclasses import dataclass, field
from numbers import Real
from typing import TypeAlias

Arc: TypeAlias = tuple[int, Real]
AdjacencyList: TypeAlias = list[list[Arc]]


@dataclass(slots=True, order=True, frozen=True)
class QueueItem:
    vertex: int = field(compare=False)
    weight: Real


# TODO: tests


def dijkstra_one_to_all(graph: AdjacencyList, source: int = 0) -> list[Real]:
    """Return the list of distances from all vertices to the source vertex.

    Unreachable vertices will be assigned a distances of float('inf').

    Complexity: O(m + n lg m) if weights are non-negative.
    """
    n = len(graph)

    distances = [float('inf') for _ in range(n)]
    distances[source] = 0

    queue = [QueueItem(source, 0)]
    while queue:
        item = heapq.heappop(queue)

        if item.weight != distances[item.vertex]:
            continue

        for w, arc_weight in graph[item.vertex]:
            if item.weight + arc_weight < distances[w]:
                distances[w] = item.weight + arc_weight
                heapq.heappush(queue, QueueItem(w, distances[w]))

    return distances
