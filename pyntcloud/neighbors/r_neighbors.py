
def r_neighbors(points, r):
    """ Get indices of all neartest neighbors with a distance < r for each point
    
    Parameters
    ----------
    kdtree: pyntcloud.structrues.KDTree
        The KDTree built on top of the points in point cloud
    
    r: float
        Maximum distance to consider a neighbor
        
    Returns
    -------
    r_neighbors: (N, X) array of lists
        Where N = kdtree.data.shape[0]
        X varies for each point
    """

    return  