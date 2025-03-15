import pytest

import numpy as np
import pandas as pd

from pyntcloud import PyntCloud


def test_default_number_of_voxels_per_axis(simple_pyntcloud):
    voxelgrid_id = simple_pyntcloud.add_structure("voxelgrid")
    voxelgrid = simple_pyntcloud.structures[voxelgrid_id]
    assert voxelgrid.n_voxels == 1
    assert np.all(voxelgrid.voxel_x == 0)
    assert np.all(voxelgrid.voxel_y == 0)
    assert np.all(voxelgrid.voxel_z == 0)
    assert np.all(voxelgrid.voxel_n == 0)
    feature_vector = voxelgrid.get_feature_vector()
    np.testing.assert_array_equal(feature_vector, np.array([[[1.0]]]))
    neighbors = voxelgrid.get_voxel_neighbors(0)
    assert neighbors == [0]


@pytest.mark.parametrize(
    "n_x, n_y, n_z, expected_voxel_n",
    [
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
        (5, 5, 2, [0, 0, 12, 24, 49, 49]),
    ],
)
def test_expected_voxel_n_for_different_number_of_voxels_per_axis(
    simple_pyntcloud, n_x, n_y, n_z, expected_voxel_n
):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid", n_x=n_x, n_y=n_y, n_z=n_z
    )
    voxelgrid = simple_pyntcloud.structures[voxelgrid_id]
    assert np.all(voxelgrid.voxel_n == expected_voxel_n)


def test_sizes_override_number_of_voxels_per_axis(simple_pyntcloud):
    voxelgrid_id = simple_pyntcloud.add_structure(
        "voxelgrid", size_x=0.2, size_y=0.2, size_z=0.2
    )
    voxelgrid = simple_pyntcloud.structures[voxelgrid_id]
    assert np.all(voxelgrid.x_y_z == [5, 5, 5])
    assert voxelgrid.n_voxels == 125
    assert np.all(voxelgrid.voxel_n == [0, 0, 31, 62, 124, 124])


@pytest.mark.parametrize(
    "x,y,z",
    [
        ([0, 1.0], [0, 0.5], [0, 0.5]),
        ([0, 0.5], [0, 1.0], [0, 0.5]),
        ([0, 0.5], [0, 0.5], [0, 1.0]),
    ],
)
def test_regular_bounding_box_changes_the_shape_of_the_bounding_box(x, y, z):
    cloud = PyntCloud(
        pd.DataFrame(
            data={
                "x": np.array(x, dtype=np.float32),
                "y": np.array(y, dtype=np.float32),
                "z": np.array(z, dtype=np.float32),
            }
        )
    )

    voxelgrid_id = cloud.add_structure(
        "voxelgrid", n_x=2, n_y=2, n_z=2, regular_bounding_box=False
    )
    voxelgrid = cloud.structures[voxelgrid_id]

    irregular_last_centroid = voxelgrid.voxel_centers[-1]

    voxelgrid_id = cloud.add_structure("voxelgrid", n_x=2, n_y=2, n_z=2)
    voxelgrid = cloud.structures[voxelgrid_id]

    regular_last_centroid = voxelgrid.voxel_centers[-1]

    assert np.all(irregular_last_centroid <= regular_last_centroid)
