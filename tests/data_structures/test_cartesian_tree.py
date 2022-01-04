import operator

from hypothesis import given, strategies as st

from src.data_structures.cartesian_tree import build_cartesian_index_tree

comps = (
    None,
    operator.lt,
    operator.gt,
)


@given(st.lists(st.integers(), min_size=1), st.sampled_from(comps))
def test_inorder_in_order(values: list[int], comp):
    ct = build_cartesian_index_tree(values, comp)
    indices = list(range(len(values)))
    traversal = [node.data for node in ct.inorder_traversal()]
    assert traversal == indices


@given(st.lists(st.integers(), min_size=1), st.sampled_from(comps))
def test_heap_property(values: list[int], comp):
    ct = build_cartesian_index_tree(values, comp)

    if comp is None:
        comp = operator.lt

    for node in ct.preorder_traversal():
        value = values[node.data]
        if node.left is not None:
            value_left = values[node.left.data]
            assert not comp(value_left, value)
        if node.right is not None:
            value_right = values[node.right.data]
            assert not comp(value_right, value)
