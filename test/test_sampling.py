import pytest

from pyntcloud import PyntCloud
from pyntcloud.utils.array import point_in_array_2D

cloud = PyntCloud.from_file("data/filters_sampling_structures.ply")

def test_voxelgrid_sampling():

    with pytest.raises(KeyError):
        # missing structure
        cloud.get_sample("voxelgrid_centers")
    
    vg_id = cloud.add_structure("voxelgrid")
    
    with pytest.raises(KeyError):
        # wrong id
        cloud.get_sample("voxelgrid_centers", voxelgrid=vg_id[:-2])
    
    sample = cloud.get_sample("voxelgrid_centers", voxelgrid=vg_id)
    
    assert point_in_array_2D([0.25, 0.25, 0.25], sample)
    
