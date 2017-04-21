import pytest
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud

def test_points():
    """
    - Points must be a pandas DataFrame
    - DataFrame must have at least "x", "y" and "z" named columns
    """
    points = np.random.rand(10, 3)
    
    # not dataframe
    with pytest.raises(TypeError):
        PyntCloud(points)
    
    points = pd.DataFrame(points)
    
    # not x, y, z
    with pytest.raises(ValueError):
        PyntCloud(points)
    
    points = pd.DataFrame(points.values, columns=["x","y","z"])
    
    assert PyntCloud(points)
    
def test_clean_all_structures():
    """
    - When PyntCloud.points is re-assigned all structures must be removed
    """
    
    points = np.random.rand(10, 3)
    points = pd.DataFrame(points, columns=["x","y","z"])
    
    cloud = PyntCloud(points)
    
    cloud.add_structure("voxelgrid")
    
    assert len(cloud.voxelgrids) == 1
    
    # dummy filter
    x_above_05 = cloud.points["x"] > 0.5
    cloud.points = cloud.points[x_above_05]
    
    assert len(cloud.voxelgrids) == 0
    
