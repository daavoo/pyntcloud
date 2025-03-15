import pytest

from pandas import DataFrame

from pyntcloud import PyntCloud
from pyntcloud.utils.array import point_in_array_2D


@pytest.mark.parametrize(
    "sampling_method", ["voxelgrid_centers", "voxelgrid_centroids", "voxelgrid_nearest"]
)
@pytest.mark.usefixtures("simple_pyntcloud")
def test_voxelgrid_sampling_return_type(simple_pyntcloud, sampling_method):
    voxelgrid_id = simple_pyntcloud.add_structure("voxelgrid")

    sample = simple_pyntcloud.get_sample(sampling_method, voxelgrid_id=voxelgrid_id)
    assert sample is DataFrame

    sample = simple_pyntcloud.get_sample(
        sampling_method, voxelgrid_id=voxelgrid_id, as_PyntCloud=True
    )
    assert sample is PyntCloud


@pytest.mark.parametrize(
    "n_x,n_y,n_z,expected_n,expected_point",
    [(2, 2, 2, 2, [0.25, 0.25, 0.25]), (2, 1, 1, 2, [0.25, 0.5, 0.5])],
)
@pytest.mark.usefixtures("simple_pyntcloud")
def test_voxelgrid_centers_expected_values(
    simple_pyntcloud, n_x, n_y, n_z, expected_n, expected_point
):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid", n_x=n_x, n_y=n_y, n_z=n_z
    )
    sample = simple_pyntcloud.get_sample("voxelgrid_centers", voxelgrid_id=voxelgrid_id)
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.values)


@pytest.mark.parametrize(
    "n_x,n_y,n_z,expected_n,expected_point",
    [(2, 2, 2, 2, [0.2, 0.2, 0.2]), (2, 1, 1, 2, [0.2, 0.2, 0.2])],
)
@pytest.mark.usefixtures("simple_pyntcloud")
def test_voxelgrid_centroids_expected_values(
    simple_pyntcloud, n_x, n_y, n_z, expected_n, expected_point
):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid", n_x=n_x, n_y=n_y, n_z=n_z
    )
    sample = simple_pyntcloud.get_sample(
        "voxelgrid_centroids", voxelgrid_id=voxelgrid_id
    )
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.values)


@pytest.mark.parametrize(
    "n_x,n_y,n_z,n_points,expected_n,expected_point",
    [
        (2, 2, 2, 1, 2, [0.2, 0.2, 0.2]),
        (2, 2, 2, 2, 4, [0.1, 0.1, 0.1]),
        (2, 1, 1, 1, 2, [0.5, 0.5, 0.5]),
    ],
)
@pytest.mark.usefixtures("simple_pyntcloud")
def test_voxelgrid_nearest_expected_values(
    simple_pyntcloud, n_x, n_y, n_z, n_points, expected_n, expected_point
):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid", n_x=n_x, n_y=n_y, n_z=n_z
    )
    sample = simple_pyntcloud.get_sample(
        "voxelgrid_nearest", voxelgrid_id=voxelgrid_id, n=n_points
    )
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.loc[:, ["x", "y", "z"]].values)


@pytest.mark.parametrize(
    "size_x,expected_n,expected_in,expected_not_in",
    [
        (0.1, 6, [0.0, 0.0, 0.0], [1.2, 1.2, 1.2]),
        (0.2, 4, [0.1, 0.1, 0.1], [0.9, 0.9, 0.9]),
    ],
)
@pytest.mark.usefixtures("simple_pyntcloud")
def test_voxelgrid_highest_expected_values(
    simple_pyntcloud, size_x, expected_n, expected_in, expected_not_in
):
    voxelgrid_id = simple_pyntcloud.add_structure("voxelgrid", size_x=size_x)
    sample = simple_pyntcloud.get_sample("voxelgrid_highest", voxelgrid_id=voxelgrid_id)

    assert len(sample) == expected_n
    assert point_in_array_2D(expected_in, sample.loc[:, ["x", "y", "z"]].values)
    assert not point_in_array_2D(expected_not_in, sample.loc[:, ["x", "y", "z"]].values)
