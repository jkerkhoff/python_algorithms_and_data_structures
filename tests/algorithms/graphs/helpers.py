from hypothesis import strategies as st


@st.composite
def adjacency_lists(draw: st.DrawFn,
                    *,
                    min_vertices: int = 0,
                    max_vertices: int = 50) -> list[list[int]]:
    vertex_count = draw(st.integers(min_vertices, max_vertices))
    adj = [[] for _ in range(vertex_count)]
    for u in range(vertex_count - 1):
        up_edges = draw(st.sets(st.integers(u + 1, vertex_count - 1)))
        for v in up_edges:
            adj[u].append(v)
            adj[v].append(u)
    return adj
