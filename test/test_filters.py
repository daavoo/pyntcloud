import os
import pytest
from pyntcloud import PyntCloud


path = os.path.abspath(os.path.dirname(__file__))
cloud = PyntCloud.from_file(path + "/data/filters.ply")

def test_kdtree_filters():
    with pytest.raises(TypeError):
        cloud.get_filter("ROR")

    kdtree = cloud.add_structure("kdtree")

    with pytest.raises(KeyError):
        cloud.get_filter("ROR", kdtree="K(12)", k=2, r=0.2)
    
    f = cloud.get_filter("ROR", kdtree=kdtree, k=2, r=0.2)

    assert f.argmin() == 3

    with pytest.raises(TypeError):
        cloud.get_filter("SOR", kdtree=kdtree, k=2)

    f = cloud.get_filter("SOR", kdtree="K(16)", k=2, z_max=0.5)

    assert f.argmin() == 3


def test_xyz_filters():
    bound = {
        "min_x": 0.4,
        "max_x": 0.6,
        "min_y": 0.4,
        "max_y": 0.6
    }

    f = cloud.get_filter("BBOX", **bound)

    assert f.argmax() == 3
