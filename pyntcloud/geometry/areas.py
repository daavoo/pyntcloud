#  HAKUNA MATATA

"""
Areas

"""
import numpy as np
from .vector import cross, normalize
from .plane import plane_def_by, project_on_plane

       
def coplanar_area(points, plane_normal=None):
    """ Area of the coplanar polygon formed by the given points.
    
    Parameters
    ----------        
    points: array
        The vertices of the selected area, the points are expected to be coplanar.
        Expected format:
            array([
            [x1,y1,z1],
            ...,
            [xn,yn,zn]])
            
    Returns
    -------
    area : float
        The area of the polygon formed by the given coplanar points.
    
    """
    
    if not plane_normal:
        
        p, normal = plane_def_by(points[:3])
    
    else:
        normal = normalize(plane_normal)
    
    #: get an array with the first point positioned as last
    points_rolled = np.roll(points, len(points) - 1, axis=0)
    
    cross_product = cross(points, points_rolled)
    
    summed = np.sum(cross_product, axis=0)
    
    total = np.dot(summed, normal)
    
    area = 0.5 * abs(total)
    
    return area


def projected_area(points, plane_point, plane_normal):
    """ Area of the polygon formed by the points projected on the given plane.
    
    Parameters
    ----------        
    points: array
        The vertices of the selected area.Expected format:
            array([
            [x1,y1,z1],
            ...,
            [xn,yn,zn]])
    

    Returns
    -------
    area : float
        The area of the polygon formed by the given coplanar points.
    
    """
    
    points = project_on_plane(points, plane_point, plane_normal)
    
    area = coplanar_area(points, plane_normal=plane_normal)
    
    return area

