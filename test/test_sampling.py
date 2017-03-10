import os
import pytest

from pyntcloud import PyntCloud
from pyntcloud.utils.array import point_in_array_2D

path = os.path.abspath(os.path.dirname(__file__))


def test_voxelgrid_sampling():
    cloud = PyntCloud.from_file(path + "\\data\\sampling\\voxelgrid.ply")
    with pytest.raises(TypeError):
        cloud.get_sample("voxelgrid_centers")
    
    vg_id = cloud.add_structure("voxelgrid")
    
    with pytest.raises(KeyError):
        cloud.get_sample("voxelgrid_centers", voxelgrid=vg_id[:-2])
    
    sample = cloud.get_sample("voxelgrid_centers", voxelgrid=vg_id)
    
    assert point_in_array_2D([0.25, 0.25, 0.25], sample)

    sample = cloud.get_sample("voxelgrid_centroids", voxelgrid=vg_id)
    
    assert point_in_array_2D([0.2, 0.2, 0.2], sample)

    sample = cloud.get_sample("voxelgrid_nearest", voxelgrid=vg_id)
    
    assert point_in_array_2D([0.9, 0.9, 0.9], sample)

def test_mesh_sampling():
    cloud = PyntCloud.from_file(path + "\\data\\sampling\\mesh.ply")
    with pytest.raises(TypeError):
        sample = cloud.get_sample("random_mesh")
    
    sample = cloud.get_sample("random_mesh", n=100)
    
    assert len(sample) == 100
    assert all(sample.max(0) <= cloud.xyz.max(0))
    assert all(sample.min(0) >= cloud.xyz.min(0))

def test_points_sampling():
    cloud = PyntCloud.from_file(path + "\\data\\sampling\\voxelgrid.ply")
    with pytest.raises(TypeError):
        sample = cloud.get_sample("random_points")
    
    sample = cloud.get_sample("random_points", n=1)
    
    assert point_in_array_2D(sample, cloud.xyz)
    
    
