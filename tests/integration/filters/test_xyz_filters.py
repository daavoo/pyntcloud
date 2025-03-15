import pytest

from numpy.testing import assert_array_equal


@pytest.mark.usefixtures("simple_pyntcloud")
def test_BBOX_default_values(simple_pyntcloud):
    """
    Default bounding box values are infinite so all points
    should pass the filter.
    """
    result = simple_pyntcloud.get_filter("BBOX")
    assert all(result)


@pytest.mark.parametrize(
    "bounding_box,expected_result",
    [
        (
            {"min_x": 0.4, "max_x": 0.6, "min_y": 0.4, "max_y": 0.6},
            [False, False, False, True, False, False],
        ),
        (
            {
                "min_x": 0.4,
            },
            [False, False, False, True, True, True],
        ),
        (
            {
                "max_x": 1.0,
            },
            [True, True, True, True, True, False],
        ),
    ],
)
@pytest.mark.usefixtures("simple_pyntcloud")
def test_BBOX_expected_results(simple_pyntcloud, bounding_box, expected_result):
    result = simple_pyntcloud.get_filter("BBOX", **bounding_box)
    assert_array_equal(result, expected_result)
