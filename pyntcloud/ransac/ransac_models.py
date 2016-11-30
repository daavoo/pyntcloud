#  HAKUNA MATATA

"""
Geometric Models for use in ransac shape fitting
"""

import numpy as np



class PlaneModel(object):
    """ A model for fitting a plane to a point cloud.
    """
    
    def __init__(self):
        self.k = 3
        
    def fit(self, k_points):
        """ Fit a plane to the given k_points.
        """
        v1 = k_points[1] - k_points[0]
        v2 = k_points[2] - k_points[0]
        #: pick one of the 3 points to represent the point of the plane
        self.point = k_points[0]
        #: the normal of the plane is the cross product between the 2 vectors
        normal = np.cross(v1,v2)
        self.normal = normal / np.linalg.norm(normal)
        
    def get_error(self, test_points):
        """ Get the distances between the test_points and the plane.
        """
        vectors = test_points - self.point
        scalars = np.dot(vectors, self.normal)

        return
