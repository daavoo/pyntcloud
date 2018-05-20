import pytest

import numpy as np

from pyntcloud.structures import VoxelGrid


@pytest.mark.usefixtures("simple_pyntcloud")
def test_VoxelGrid_default_number_of_voxels_per_axis(simple_pyntcloud):
    voxelgrid = VoxelGrid(simple_pyntcloud)
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
