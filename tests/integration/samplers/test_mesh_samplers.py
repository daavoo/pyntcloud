import pytest

from pandas import DataFrame

from pyntcloud import PyntCloud


def test_mesh_random_sampling_return_type(diamond):
    sample = diamond.get_sample("mesh_random", n=10, rgb=True, normals=True)
    assert sample is DataFrame

    sample = diamond.get_sample(
        "mesh_random", n=10, rgb=True, normals=True, as_PyntCloud=True
    )
    assert sample is PyntCloud


@pytest.mark.parametrize("n", [1, 5, 10, 50, 100])
def test_mesh_random_sampling_n_argument(diamond, n):
    sample = diamond.get_sample("mesh_random", n=n, rgb=True, normals=True)
    assert len(sample) == n


@pytest.mark.parametrize(
    "rgb,normals", [(False, False), (True, False), (True, True), (False, True)]
)
def test_mesh_random_sampling_rgb_normals_optional_arguments(diamond, rgb, normals):
    sample = diamond.get_sample("mesh_random", n=10, rgb=rgb, normals=normals)

    for x in ["red", "green", "blue"]:
        assert (x in sample) == rgb

    for x in ["nx", "ny", "nz"]:
        assert (x in sample) == normals


@pytest.mark.parametrize("n", [1, 5, 10, 50, 100])
@pytest.mark.usefixtures("diamond")
def test_mesh_random_sampling_sampled_points_bounds(diamond, n):
    sample = diamond.get_sample("mesh_random", n=n, rgb=True, normals=True)

    assert all(sample[["x", "y", "z"]].values.max(0) <= diamond.xyz.max(0))
    assert all(sample[["x", "y", "z"]].values.min(0) >= diamond.xyz.min(0))
