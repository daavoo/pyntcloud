
import numpy as np
from ..geometry.areas import triangle_area_multi

def mesh_sampling(v1, v2, v3, n):
    """ Sample n points from the mesh defined by v1, v2, v3.

    Parameters
    ----------
    v1: (N, 3) ndarray
        Contains the x,y,z coordinates of points considered as the
        first vertex of each triangle.
    v2: (N, 3) ndarray
    v3: (N, 3) ndarray
    n: int
        Number of points to be sampled
    
    Returns
    -------
    sampled_points: (n, 3)
        Points sampled from the mesh triangles

    Notes
    -----
    v1[i], v2[i], v3[i] represent the ith triangle

    """
    areas = triangle_area_multi(v1, v2, v3)
    probabilities = areas / np.sum(areas)
    random_idx = np.random.choice(np.arange(len(areas)), size=n, p=probabilities)
    
    v1 = v1[random_idx]
    v2 = v2[random_idx]
    v3 = v3[random_idx]
    
    # (n, 1) the 1 is for broadcasting
    u = np.random.rand(n, 1)
    v = np.random.rand(n, 1)
    is_a_problem = u + v > 1
    
    u[is_a_problem] = 1 - u[is_a_problem]
    v[is_a_problem] = 1 - v[is_a_problem]
    
    result = (v1 * u) + (v2 * v) + ((1 - (u + v)) * v3)
    
    return result