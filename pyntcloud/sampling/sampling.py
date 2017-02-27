#  HAKUNA MATATA

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from ..geometry.areas import triangle_area_multi



def random_sampling(points, n):

    return points[np.random.randint(0, points.shape[0], size=n)]


def mesh_sampling(v1, v2, v3, n):
    
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

def voxelgrid_centers(voxelgrid):
    return voxelgrid.voxel_centers[np.unique(voxelgrid.voxel_n)]

def voxelgrid_centroids(voxelgrid):
    df = pd.DataFrame(voxelgrid.points, columns=["x", "y", "z"])
    df["voxel_n"] = voxelgrid.voxel_n
    return df.groupby("voxel_n").mean().values

def voxelgrid_nearest(voxelgrid):
    nonzero_centers = voxelgrid.voxel_centers[np.unique(voxelgrid.voxel_n)]
    kdt = cKDTree(voxelgrid.points)
    dist, nearest_indices =  kdt.query(nonzero_centers, n_jobs=-1)
    return voxelgrid.points[nearest_indices]
