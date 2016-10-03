#  HAKUNA MATATA

"""
Octree filters
"""
import numpy as np

def octree_subsample(octree, k):
    """ Compute an Octree subsample filter on the given octree
    
    Parameters
    ----------         
    octree : pyntcloud's VoxelGrid instance
        The Octree's structure that will be used to subsamble the point cloud
    """
    
    points = octree.xyz
    centroids = [['centroid_x','centroid_y','centroid_z']].as_matrix()
    
    octree['distances'] = np.linalg.norm(points - centroids, axis=1)