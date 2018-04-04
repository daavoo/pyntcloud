import pytest

from pandas import DataFrame

from pyntcloud import PyntCloud
from pyntcloud.utils.array import point_in_array_2D


@pytest.mark.usefixtures("simple_pyntcloud")
def test_mesh_random_sampling_return_type(simple_pyntcloud):
    sample = simple_pyntcloud.get_sample(
        "points_random",
        n=5)
    assert type(sample) == DataFrame

    sample = simple_pyntcloud.get_sample(
        "points_random",
        n=5,
        as_PyntCloud=True)
    assert type(sample) == PyntCloud

@pytest.mark.parametrize("n", [
    1,
    5,
    6
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_RandomPointsSampler_n_argument(simple_pyntcloud, n):
    sample = simple_pyntcloud.get_sample(
        "points_random",
        n=n)
    assert len(sample) == n


@pytest.mark.usefixtures("simple_pyntcloud")
def test_RandomPointsSampler_raises_ValueError_on_invalid_n(simple_pyntcloud):
    with pytest.raises(ValueError):
        simple_pyntcloud.get_sample(
            "points_random",
            n=10)


@pytest.mark.usefixtures("simple_pyntcloud")
def test_RandomPointsSampler_sampled_points_are_from_original(simple_pyntcloud):
    for i in range(10):
        sample = simple_pyntcloud.get_sample(
            "points_random",
            n=1)
        assert point_in_array_2D(sample, simple_pyntcloud.xyz)

