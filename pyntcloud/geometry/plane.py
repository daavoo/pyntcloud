#  HAKUNA MATATA

import numpy as np

class Plane():

    def __init__(self, point=None, normal=None):
        self.point = point
        self.normal= normal
        # for ransac
        self.k = 3
    
    def from_three_points(self, points):
        normal = np.cross(points[1] - points[0], points[2] - points[0])
        self.point = points[0]
        self.normal = normal / np.linalg.norm(normal)
    
    def from_equation(self, a, b, c, d):
        normal = np.array([a,b,c])
        point = np.array([-d / a, -d / b, -d / c])
        self.point = point
        self.normal = normal

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
        
    def fit(self, points):
        self.from_three_points(points)
    
    def get_error(self, points):
        return self.get_projections(points, only_distances=True)     

