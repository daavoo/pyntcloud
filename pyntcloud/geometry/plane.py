#  HAKUNA MATATA

import numpy as np

class Plane():

    def __init__(self, point=None, normal=None):
        self.point = point
        self.normal= normal / np.linalg.norm(normal)
        # for ransac
        self.k = 3
    
    @classmethod
    def from_three_points(cls, points):
        normal = np.cross(points[1] - points[0], points[2] - points[0])
        return cls(point=points[0], normal=normal)

    @classmethod
    def from_equation(cls, a, b, c, d):
        normal = np.array([a,b,c])
        point = np.array([-d / a, -d / b, -d / c])
        return cls(point=point, normal=normal)

    def get_equation(self):
        a, b, c = self.normal
        d = - np.dot(self.normal, self.point)
        return a, b, c, d
    
    def get_projections(self, points, only_distances=False):
        vectors = points - self.point
        distances = np.abs(np.dot(vectors, self.normal))
        if only_distances:
            return distances
        projections = points - (distances[:,None] * self.normal)
        return distances, projections

    def contains(self, a_point):
        d1 = - np.dot(self.normal, self.point)
        d2 = - np.dot(self.normal, a_point)
        return True if d1 == d2 else False

    # RANSAC METHODS
    
    def fit(self, points):
        normal = np.cross(points[1] - points[0], points[2] - points[0])
        self.point = points[0]
        self.normal = normal / np.linalg.norm(normal)
    
    def get_error(self, points):
        return self.get_projections(points, only_distances=True)     
    
    def are_valid(self, points):
        return True




