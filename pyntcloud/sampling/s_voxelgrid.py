
import numpy as np
from scipy.spatial import cKDTree

def voxelgrid_centers(voxelgrid):
    """ Returns the points that represent each occupied voxel's center.

    Parameters
    ----------
    voxelgrid: Voxelgrid instance
        From ..structures.voxelgrid class
    
    Returns
    -------
    (N, 3) ndarray
        Representing each occupied voxel's center.
        N is the number of occupied voxels.
    """

    return voxelgrid.voxel_centers[np.unique(voxelgrid.voxel_n)]

def voxelgrid_centroids(voxelgrid):
    """ Returns the centroid of each group of points inside each occupied voxel.

    Parameters
    ----------
    voxelgrid: Voxelgrid instance
        From ..structures.voxelgrid class
    
    Returns
    -------
    (N, 3) ndarray
        Representing the centroid of each group of points inside each occupied voxel.
        N is the number of occupied voxels.
    """

    df = pd.DataFrame(voxelgrid.points, columns=["x", "y", "z"])
    df["voxel_n"] = voxelgrid.voxel_n
    return df.groupby("voxel_n").mean().values

def voxelgrid_nearest(voxelgrid):
    """ Returns the point closest to each occupied voxel's center.

    Parameters
    ----------
    voxelgrid: Voxelgrid instance
        From ..structures.voxelgrid class
    
    Returns
    -------
    (N, 3) ndarray
        Representing the point closest to each occupied voxel's center.
        N is the number of occupied voxels.
    """

    nonzero_centers = voxelgrid.voxel_centers[np.unique(voxelgrid.voxel_n)]
    kdt = cKDTree(voxelgrid.points)
    dist, nearest_indices =  kdt.query(nonzero_centers, n_jobs=-1)
    return voxelgrid.points[nearest_indices]