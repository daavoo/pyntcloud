
from ..ransac import ransac
from ..geometry import Plane, Sphere

def is_plane(points):
    """ Returns wich points belong to the best ransac Plane found.

    Parameters
    ----------
    points: (N,3) ndarray
         x, y, z coordinates of the given 'N' points.
    
    Returns
    -------
    is_plane: (N,) ndarray
        Boolean array indicating wich points are considered inliers of
        the best Plane found using ransac.
    """
    return [ransac(points, Plane())]

def is_sphere(points):
    """ Returns wich points belong to the best ransac Sphere found.

    Parameters
    ----------
    points: (N,3) ndarray
         x, y, z coordinates of the given 'N' points.
    
    Returns
    -------
    is_sphere: (N,) ndarray
        Boolean array indicating wich points are considered inliers of
        the best Sphere found using ransac.
    """
    return [ransac(points, Sphere())]