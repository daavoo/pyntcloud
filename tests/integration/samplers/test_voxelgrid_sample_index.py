import pandas as pd
import pytest

from pyntcloud import PyntCloud


@pytest.mark.parametrize("method", ["voxelgrid_nearest", "voxelgrid_highest"])
def test_voxelgrid_sampling_after_points_selection(simple_pyntcloud, method):
    cloud = simple_pyntcloud
    cloud.points = cloud.points.loc[cloud.points["x"] > 0.3]
    reference = PyntCloud(cloud.points.reset_index(drop=True))
    grid_id = cloud.add_structure("voxelgrid")
    reference_grid_id = reference.add_structure("voxelgrid")

    expected = reference.get_sample(method, voxelgrid_id=reference_grid_id)
    sample = cloud.get_sample(method, voxelgrid_id=grid_id)

    pd.testing.assert_frame_equal(sample, expected)
    assert cloud.points.index.tolist() == [3, 4, 5]
