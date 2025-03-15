import pytest

from numpy.testing import assert_array_equal


@pytest.mark.parametrize("kdtree_id", ["FOO", "K", "K(10)", "K(16", "K16)", "K16"])
@pytest.mark.usefixtures("pyntcloud_with_kdtree_and_kdtree_id")
def test_ROR_raises_KeyError_if_id_is_not_valid(
    pyntcloud_with_kdtree_and_kdtree_id, kdtree_id
):
    cloud, true_id = pyntcloud_with_kdtree_and_kdtree_id
    with pytest.raises(KeyError):
        cloud.get_filter("ROR", kdtree_id=kdtree_id, k=2, r=0.2)


@pytest.mark.parametrize("kdtree_id", ["FOO", "K", "K(10)", "K(16", "K16)", "K16"])
@pytest.mark.usefixtures("pyntcloud_with_kdtree_and_kdtree_id")
def test_SOR_raises_KeyError_if_id_is_not_valid(
    pyntcloud_with_kdtree_and_kdtree_id, kdtree_id
):
    cloud, true_id = pyntcloud_with_kdtree_and_kdtree_id
    with pytest.raises(KeyError):
        cloud.get_filter("SOR", kdtree_id=kdtree_id, k=2, z_max=0.5)


@pytest.mark.parametrize(
    "k,r,expected_result",
    [
        (2, 0.2, [True, True, True, False, True, True]),
        (3, 0.2, [False, True, False, False, False, False]),
        (3, 0.35, [True, True, True, False, False, False]),
    ],
)
@pytest.mark.usefixtures("pyntcloud_with_kdtree_and_kdtree_id")
def test_ROR_expected_results(
    pyntcloud_with_kdtree_and_kdtree_id, k, r, expected_result
):
    cloud, kdtree_id = pyntcloud_with_kdtree_and_kdtree_id
    result = cloud.get_filter("ROR", kdtree_id=kdtree_id, k=k, r=r)
    assert_array_equal(result, expected_result)


@pytest.mark.parametrize(
    "k,z_max,expected_result", [(2, 0.5, [True, True, True, False, True, True])]
)
@pytest.mark.usefixtures("pyntcloud_with_kdtree_and_kdtree_id")
def test_SOR_expected_results(
    pyntcloud_with_kdtree_and_kdtree_id, k, z_max, expected_result
):
    cloud, kdtree_id = pyntcloud_with_kdtree_and_kdtree_id
    result = cloud.get_filter("SOR", kdtree_id=kdtree_id, k=k, z_max=z_max)
    assert_array_equal(result, expected_result)
