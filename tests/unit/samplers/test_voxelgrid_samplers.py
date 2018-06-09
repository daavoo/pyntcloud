import pytest

from pyntcloud.samplers import (
    VoxelgridCentersSampler,
    VoxelgridCentroidsSampler,
    VoxelgridNearestSampler,
    VoxelgridHighestSampler
)
from pyntcloud.utils.array import point_in_array_2D


@pytest.mark.parametrize("n_x, n_y, n_z,expected_n,expected_point", [
    (
        2, 2, 2,
        2,
        [0.25, 0.25, 0.25]
    ),
    (
        2, 1, 1,
        2,
        [0.25, 0.5, 0.5]
    )
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_VoxelgridCentersSampler_expected_values(simple_pyntcloud, n_x, n_y, n_z, expected_n, expected_point):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid",
        n_x=n_x,
        n_y=n_y,
        n_z=n_z)
    sampler = VoxelgridCentersSampler(
        pyntcloud=simple_pyntcloud,
        voxelgrid_id=voxelgrid_id)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.values)


@pytest.mark.parametrize("n_x, n_y, n_z,expected_n,expected_point", [
    (
        2, 2, 2,
        2,
        [0.2, 0.2, 0.2]
    ),
    (
        2, 1, 1,
        2,
        [0.2, 0.2, 0.2]
    )
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_VoxelgridCentroidsSampler_expected_values(simple_pyntcloud, n_x, n_y, n_z, expected_n, expected_point):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid",
        n_x=n_x,
        n_y=n_y,
        n_z=n_z)
    sampler = VoxelgridCentroidsSampler(
        pyntcloud=simple_pyntcloud,
        voxelgrid_id=voxelgrid_id)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.values)


@pytest.mark.parametrize("n_x, n_y, n_z,n_points,expected_n,expected_point", [
    (
        2, 2, 2,
        1,
        2,
        [0.2, 0.2, 0.2]
    ),
    (
        2, 2, 2,
        2,
        4,
        [0.1, 0.1, 0.1]
    ),
    (
        2, 1, 1,
        1,
        2,
        [0.5, 0.5, 0.5]
    )
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_VoxelgridNearestSampler_expected_values(simple_pyntcloud, n_x, n_y, n_z, n_points, expected_n, expected_point):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid",
        n_x=n_x,
        n_y=n_y,
        n_z=n_z)
    sampler = VoxelgridNearestSampler(
        pyntcloud=simple_pyntcloud,
        voxelgrid_id=voxelgrid_id,
        n=n_points)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_point, sample.loc[:, ["x", "y", "z"]].values)


def test_VoxelgridNearestSampler_keeps_original_scalar_fields(pyntcloud_with_rgb_and_normals):
    voxelgrid_id = pyntcloud_with_rgb_and_normals.add_structure(
        "voxelgrid")
    sampler = VoxelgridNearestSampler(
        pyntcloud=pyntcloud_with_rgb_and_normals,
        voxelgrid_id=voxelgrid_id)
    sampler.extract_info()

    sample = sampler.compute()
    assert "red" in sample


@pytest.mark.parametrize("size_x,expected_n,expected_in,expected_not_in", [
    (
        0.1,
        6,
        [0., 0., 0.],
        [1.2, 1.2, 1.2]
    ),
    (
        0.2,
        4,
        [0.1, 0.1, 0.1],
        [0.9, 0.9, 0.9]
    )
])
@pytest.mark.usefixtures("simple_pyntcloud")
def test_VoxelgridHighestSampler_expected_values(simple_pyntcloud, size_x, expected_n, expected_in, expected_not_in):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid",
        size_x=size_x)
    sampler = VoxelgridHighestSampler(
        pyntcloud=simple_pyntcloud,
        voxelgrid_id=voxelgrid_id)
    sampler.extract_info()

    sample = sampler.compute()
    assert len(sample) == expected_n
    assert point_in_array_2D(expected_in, sample.loc[:, ["x", "y", "z"]].values)
    assert not point_in_array_2D(expected_not_in, sample.loc[:, ["x", "y", "z"]].values)


def test_VoxelgridHighestSampler_keeps_original_scalar_fields(pyntcloud_with_rgb_and_normals):
    voxelgrid_id = pyntcloud_with_rgb_and_normals.add_structure(
        "voxelgrid")
    sampler = VoxelgridHighestSampler(
        pyntcloud=pyntcloud_with_rgb_and_normals,
        voxelgrid_id=voxelgrid_id)
    sampler.extract_info()

    sample = sampler.compute()
    assert "red" in sample
