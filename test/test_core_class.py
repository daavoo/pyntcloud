import pytest
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud

def test_points():
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

