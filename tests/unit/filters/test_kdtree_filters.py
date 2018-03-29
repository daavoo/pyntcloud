import pytest

from numpy.testing import assert_array_equal

from pyntcloud.filters.kdtree import (
    KDTreeFilter,
    RadiusOutlierRemovalFilter,
    StatisticalOutlierRemovalFilter
)

@pytest.mark.parametrize("kdtree_id", [
    "FOO",
    "K",
    "K(10)",
    "K(16",
    "K16)",
    "K16"
])
@pytest.mark.usefixtures("pyntcloud_with_kdtree")
def test_KDTreeFilter_raises_KeyError_if_id_is_not_valid(pyntcloud_with_kdtree, kdtree_id):
    filter = KDTreeFilter(pyntcloud=pyntcloud_with_kdtree, kdtree_id=kdtree_id)
    with pytest.raises(KeyError):
        filter.extract_info()


@pytest.mark.parametrize("k,r,expected_result", [
    (
        2,
        0.2,
        [True, True, True, False, True, True]
    ),
    (
        3,
        0.2,
        [False, True, False, False, False, False]
    ),
    (
        3,
        0.35,
        [True, True, True, False, False, False]
    )
])
@pytest.mark.usefixtures("pyntcloud_with_kdtree")
def test_RORFilter_expected_results(pyntcloud_with_kdtree, k, r, expected_result):
    filter = RadiusOutlierRemovalFilter(
        pyntcloud=pyntcloud_with_kdtree,
        kdtree_id="K(16)",
        k=k,
        r=r
    )
    filter.extract_info()
    result = filter.compute()

    assert_array_equal(result, expected_result)


@pytest.mark.parametrize("k,z_max,expected_result", [
    (
        2,
        0.5,
        [True, True, True, False, True, True]
    )
])
@pytest.mark.usefixtures("pyntcloud_with_kdtree")
def test_SORFilter_expected_results(pyntcloud_with_kdtree, k, z_max, expected_result):
    filter = StatisticalOutlierRemovalFilter(
        pyntcloud=pyntcloud_with_kdtree,
        kdtree_id="K(16)",
        k=k,
        z_max=z_max
    )
    filter.extract_info()
    result = filter.compute()

    assert_array_equal(result, expected_result)