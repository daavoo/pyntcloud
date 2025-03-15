import pytest

from pyntcloud.samplers import RandomPointsSampler
from pyntcloud.utils.array import point_in_array_2D


@pytest.mark.parametrize("n", [1, 5, 6])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_RandomPointsSampler_n_argument(simple_pyntcloud, n):
    sampler = RandomPointsSampler(pyntcloud=simple_pyntcloud, n=n)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == n


@pytest.mark.usefixtures("simple_pyntcloud")
def test_RandomPointsSampler_raises_ValueError_on_invalid_n(simple_pyntcloud):
    sampler = RandomPointsSampler(pyntcloud=simple_pyntcloud, n=10)
    sampler.extract_info()
    with pytest.raises(ValueError):
        sampler.compute()


@pytest.mark.usefixtures("simple_pyntcloud")
def test_RandomPointsSampler_sampled_points_are_from_original(simple_pyntcloud):
    for i in range(10):
        sampler = RandomPointsSampler(pyntcloud=simple_pyntcloud, n=1)
        sampler.extract_info()

        sample = sampler.compute()
        assert point_in_array_2D(sample, simple_pyntcloud.xyz)
