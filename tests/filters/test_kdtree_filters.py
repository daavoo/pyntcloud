import os

import pytest

from pyntcloud import PyntCloud

@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
def test_raises_TypeError_when_missing_required_argmuents():
    """
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