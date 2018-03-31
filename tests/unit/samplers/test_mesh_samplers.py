import pytest

from pyntcloud.samplers import RandomMeshSampler


@pytest.mark.parametrize("n", [
    1,
    5,
    10,
    50,
    100
])
@pytest.mark.usefixtures("diamond")
def test_RandomMeshSampler_n_argument(diamond, n):
    sampler = RandomMeshSampler(
        pyntcloud=diamond,
        n=n,
        rgb=True,
        normals=True)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == n


@pytest.mark.parametrize("rgb,normals", [
    (False, False),
    (True, False),
    (True, True),
    (False, True)
])
@pytest.mark.usefixtures("diamond")
def test_RandomMeshSampler_rgb_normals_optional_arguments(diamond, rgb, normals):
    sampler = RandomMeshSampler(
        pyntcloud=diamond,
        n=10,
        rgb=rgb,
        normals=normals)
    sampler.extract_info()

    sample = sampler.compute()
    for x in ["red", "green", "blue"]:
        assert (x in sample) == rgb

    for x in ["nx", "ny", "nz"]:
        assert (x in sample) == normals


@pytest.mark.parametrize("n", [
    1,
    5,
    10,
    50,
    100
])
@pytest.mark.usefixtures("diamond")
def test_RandomMeshSampler_sampled_points_bounds(diamond, n):
    sampler = RandomMeshSampler(
        pyntcloud=diamond,
        n=n,
        rgb=True,
        normals=True)
    sampler.extract_info()

    sample = sampler.compute()
    assert all(sample[["x", "y", "z"]].values.max(0) <= diamond.xyz.max(0))
    assert all(sample[["x", "y", "z"]].values.min(0) >= diamond.xyz.min(0))

