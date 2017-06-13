import numpy as np


class Plane(object):

    def __init__(self, point=None, normal=None):
        self.point = point
        self.normal = normal
        if normal is not None:
            self.normal /= np.linalg.norm(normal)

    def from_k_points(self, points):
        normal = np.cross(points[1] - points[0], points[2] - points[0])
        self.point = points[0]
        self.normal = normal / np.linalg.norm(normal)

    def from_equation(self, a, b, c, d):
        normal = np.array([a, b, c])
        point = np.array([-d / a, -d / b, -d / c])
        self.point = point
        self.normal = normal / np.linalg.norm(normal)

    def get_equation(self):
        a, b, c = self.normal
        d = - np.dot(self.normal, self.point)
        return a, b, c, d

    def get_projections(self, points, only_distances=False):
        vectors = points - self.point
        distances = np.abs(np.dot(vectors, self.normal))
        if only_distances:
            return distances
        projections = points - (distances[:, None] * self.normal)
        return distances, projections
