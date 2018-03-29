import os
import pytest
from pyntcloud import PyntCloud


path = os.path.abspath(os.path.dirname(__file__))
cloud = PyntCloud.from_file(path + "/data/test_data_filters.ply")


def test_kdtree_filters():
    """filters.f_kdtree.

    - Raise TypeError when missing required arguments
    - Raise KeyError when structure.id is invalid
    - Raise TypeError when wrong argument is given (k instead of r)
    - Manually check known result.

    """
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
    """filters.f_xyz.

    - Manually check known result.

    """
    cloud = PyntCloud.from_file(path + "/data/test_data_filters.ply")

    bbox = {
        "min_x": 0.4,
        "max_x": 0.6,
        "min_y": 0.4,
        "max_y": 0.6
    }

    f = cloud.get_filter("BBOX", and_apply=True, **bbox)

    assert f.argmax() == 3
    assert len(cloud.points == 1)
