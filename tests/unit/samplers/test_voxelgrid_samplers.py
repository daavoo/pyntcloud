import pytest

from pyntcloud.samplers import (
    VoxelgridCentersSampler,
    VoxelgridCentroidsSampler,
    VoxelgridNearestSampler
)
from pyntcloud.utils.array import point_in_array_2D


@pytest.mark.parametrize("x_y_z,expected_n,expected_point", [
    (
        [2, 2, 2],
        2,
        [0.25, 0.25, 0.25]
    ),
    (
        [2, 1, 1],
        2,
        [0.25, 0.5, 0.5]
    )
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_VoxelgridCentersSampler_expected_values(simple_pyntcloud, x_y_z, expected_n, expected_point):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid",
        x_y_z=x_y_z)
    sampler = VoxelgridCentersSampler(
        pyntcloud=simple_pyntcloud,
        voxelgrid_id=voxelgrid_id)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.values)


@pytest.mark.parametrize("x_y_z,expected_n,expected_point", [
    (
        [2, 2, 2],
        2,
        [0.2, 0.2, 0.2]
    ),
    (
        [2, 1, 1],
        2,
        [0.2, 0.2, 0.2]
    )
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_VoxelgridCentroidsSampler_expected_values(simple_pyntcloud, x_y_z, expected_n, expected_point):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid",
        x_y_z=x_y_z)
    sampler = VoxelgridCentroidsSampler(
        pyntcloud=simple_pyntcloud,
        voxelgrid_id=voxelgrid_id)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.values)


@pytest.mark.parametrize("x_y_z,n_points,expected_n,expected_point", [
    (
        [2, 2, 2],
        1,
        2,
        [0.2, 0.2, 0.2]
    ),
    (
        [2, 2, 2],
        2,
        4,
        [0.1, 0.1, 0.1]
    ),
    (
        [2, 1, 1],
        1,
        2,
        [0.5, 0.5, 0.5]
    )
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_VoxelgridNearestSampler_expected_values(simple_pyntcloud, x_y_z, n_points, expected_n, expected_point):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid",
        x_y_z=x_y_z)
    sampler = VoxelgridNearestSampler(
        pyntcloud=simple_pyntcloud,
        voxelgrid_id=voxelgrid_id,
        n=n_points)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.values)

