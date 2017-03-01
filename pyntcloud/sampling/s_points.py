
from random import sample

def random_sampling(points, n):
    """ Returns 'n' unique points randomly chosen

    Parameters
    ----------
    points: ndarray
        (N, X) ndarray where N is the number of points and X is
        the number of scalar fields (counting x,y,z coordinates as scalar fields).
    n: int
        Number of unique points that will be chosen.
    
    Returns
    -------
    (n, X) ndarray with sampled points.
    """
    return points[sample(range(0, points.shape[0]), n)]