import pytest

import numpy as np

from pyntcloud.structures import VoxelGrid


def test_default_number_of_voxels_per_axis(simple_pyntcloud):
    voxelgrid = VoxelGrid(cloud=simple_pyntcloud)
    voxelgrid.extract_info()
    assert voxelgrid.n_voxels == 1
    voxelgrid.compute()
    assert np.all(voxelgrid.voxel_x == 0)
    assert np.all(voxelgrid.voxel_y == 0)
    assert np.all(voxelgrid.voxel_z == 0)
    assert np.all(voxelgrid.voxel_n == 0)
    feature_vector = voxelgrid.get_feature_vector()
    np.testing.assert_array_equal(feature_vector, np.array([[[1.]]]))
    neighbors = voxelgrid.get_voxel_neighbors(0)
    assert neighbors == [0]


@pytest.mark.parametrize("n_x, n_y, n_z, expected_voxel_n", [
    (2, 1, 1, [0, 0, 0, 0, 1, 1]),
    (1, 2, 1, [0, 0, 0, 0, 1, 1]),
    (1, 1, 2, [0, 0, 0, 0, 1, 1]),
    (2, 2, 2, [0, 0, 0, 0, 7, 7]),
    (5, 1, 1, [0, 0, 1, 2, 4, 4]),
    (1, 5, 1, [0, 0, 1, 2, 4, 4]),
    (1, 1, 5, [0, 0, 1, 2, 4, 4]),
    (5, 5, 5, [0, 0, 31, 62, 124, 124]),
    (2, 5, 5, [0, 0, 6, 12, 49, 49]),
    (2, 5, 2, [0, 0, 2, 4, 19, 19]),
    (5, 2, 5, [0, 0, 11, 22, 49, 49]),
    (5, 5, 2, [0, 0, 12, 24, 49, 49])
])
def test_expected_voxel_n_for_different_number_of_voxels_per_axis(simple_pyntcloud, n_x, n_y, n_z, expected_voxel_n):
    voxelgrid = VoxelGrid(cloud=simple_pyntcloud, n_x=n_x, n_y=n_y, n_z=n_z)
    voxelgrid.extract_info()
    voxelgrid.compute()
    assert np.all(voxelgrid.voxel_n == expected_voxel_n)

