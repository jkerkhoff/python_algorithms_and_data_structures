import pytest

from hypothesis import given

from tests.helpers import with_index_permutation
from tests.algorithms.graphs.helpers import adjacency_lists

from src.algorithms.graphs.vertex_coloring import color_greedy


def check_proper_coloring(adj: list[list[int]], colors: list[int]):
    __tracebackhide__ = True

    if len(colors) != len(adj):
        pytest.fail(f"invalid coloring: "
                    f"length of adjacency list and color table do not match")

    num_colors = len(set(colors))
    for u in range(len(adj)):
        if colors[u] not in range(0, num_colors):
            pytest.fail(f"invalid coloring: vertex {u} has color {colors[u]}, "
                        f"which is not in the valid range")

        for v in adj[u]:
            if colors[v] == colors[u]:
                pytest.fail(
                    f"improper coloring: "
                    f"adjacent vertices {u} and {v} share color {colors[v]}")


@given(with_index_permutation(adjacency_lists()))
def test_color_greedy(ex):
    adj, order = ex
    colors = color_greedy(adj, order)

    check_proper_coloring(adj, colors)

    colors_used = len(set(colors))
    max_degree = max((len(e) for e in adj), default=0)
    assert colors_used <= max_degree + 1
