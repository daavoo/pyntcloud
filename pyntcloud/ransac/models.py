
import numpy as np
from abc import ABC, abstractmethod
from ..geometry import Plane, Sphere

class RansacModel(ABC):
    """ Base class for ransac models.

    Parameters
    ----------
    max_dist : float
        Treshold distance to consider a point as an inlier.

    """
    def __init__(self, max_dist=1e-4):
        self.max_dist = max_dist
    
    @abstractmethod
    def fit(self, k_points):
        pass

    @abstractmethod
    def get_distances(self, points):
        pass
    
    @abstractmethod
    def are_valid(self, k_points):
        pass

class RansacPlane(RansacModel, Plane):

    def __init__(self, max_dist=1e-4):
        RansacModel.__init__(max_dist)
        Plane.__init__()
        self.k = 3

    def fit(self, k_points):
        return self.from_three_points(k_points)
    
    def get_distances(self, points):
        return self.get_projections(points, only_distances=True)
    
    def are_valid(self, k_points):
        return True

class RansacSphere(RansacModel, Sphere):

    def __init__(self, max_dist=1e-4):
        RansacModel.__init__(max_dist)
        Sphere.__init__()
        self.k = 4

    def fit(self, k_points):
        return self.from_four_points(k_points)
    
    def get_distances(self, points):
        return self.get_projections(points, only_distances=True)ç
    
    def are_valid(self, k_points):    
        x = np.ones((4,4))
        x [:-1,:] = k_points.T
        if np.linalg.det(x) == 0:
            return False
        else:
            return True