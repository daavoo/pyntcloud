#  HAKUNA MATATA

"""
Geometric Models for use in ransac shape fitting
"""

import numpy as np
from numba import jitclass
from numba import int32, float32 
from numba_func import cross, normalize, array_minus_vector, projection_len

#: The specs for each of the geometric models
plane_spec = [
    ('k', int32),               
    ('k_points', float32[:,:]),
    ('point', float32[:]),
    ('normal', float32[:]),
    ('test_points', float32[:,:]),
]

sphere_spec = [
    ('k', int32),               
    ('k_points', float32[:,:]),
    ('point', float32[:]),
    ('normal', float32[:]),
    ('test_points', float32[:,:]),
]


@jitclass(plane_spec)
class PlaneModel(object):
    """ A model for fitting a plane to a point cloud.
    """
    
    def __init__(self):
        self.k = 3
        
    def fit(self, k_points):
        """ Fit a plane to the given k_points.
        """
        
        #: get 2 vectors
        v1 = k_points[1] - k_points[0]
        v2 = k_points[2] - k_points[0]
        
        #: pick one of the 3 points to represent the point of the plane
        self.point = k_points[0]
        
        #: the normal of the plane is the cross product between the 2 vectors
        normal = cross(v1,v2)
        
        normalize(normal)
        
        self.normal = normal
        
    def get_error(self, test_points):
        """ Get the distances between the test_points and the plane.
        """

        #: get vectors from the plane's point to all the given test points
        vectors = test_points - self.point
        
        #: get the scalar projection of the vectors onto the plane's normal
        scalars = np.dot(vectors, self.normal)
        

        
        return errors


#: just in case
plane_normal = normalize(plane_normal)

#: get vectors from the plane's point to all the given test points
vectors = array_minus_vector(points, plane_point)

#: get the scalar projection of the vectors onto the plane's normal
scalars = np.dot(vectors, plane_normal)

#: get the orthogonal-projection vectors
orthogonal_projection = scalars_dot_vector(scalars, plane_normal)

#: substract the projections to each point
proj_points = points - orthogonal_projection

if return_distances:
    return proj_points, norm_all(orthogonal_projection)
else:
    return proj_points


@jitclass(sphere_spec)
class SphereModel(object):
    """ A model for fitting a sphere to a point cloud.
    """
    
    def __init__(self):
        self.k = 2
        
    def fit(self, k_points):
        """ Fit a plane to the given k_points.
        """
        
    def get_error(self, test_points):
        """ Get the distances between the test_points and the plane.
        """
                
        return 
