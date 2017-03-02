
from ..structures import KDTree

def k_neighbors(points, k, kdtree):

    # [1] to select indices and ignore distances
    # [:,1:] to discard self-neighbor
    return kdtree.query(points, k=k+1, n_jobs=-1)[1][:,1:]