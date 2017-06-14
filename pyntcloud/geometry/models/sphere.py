import numpy as np
from .base import GeometryModel


class Sphere(GeometryModel):

    def __init__(self, center=None, radius=None):
        self.center = center
        self.radius = radius

    def from_k_points(self, points):
        # adapted from
        # http://www.abecedarical.com/zenosamples/zs_sphere4pts.html

        X = np.zeros((4, 4))

        # Get the Minors

        for i in range(4):
            X[i, 0] = points[i, 0]
            X[i, 1] = points[i, 1]
            X[i, 2] = points[i, 2]
            X[i, 3] = 1
        m11 = np.linalg.det(X)

        for i in range(4):
            X[i, 0] = np.dot(points[i], points[i])
            X[i, 1] = points[i, 1]
            X[i, 2] = points[i, 2]
            X[i, 3] = 1
        m12 = np.linalg.det(X)

        for i in range(4):
            X[i, 0] = np.dot(points[i], points[i])
            X[i, 1] = points[i, 0]
            X[i, 2] = points[i, 2]
            X[i, 3] = 1
        m13 = np.linalg.det(X)

        for i in range(4):
            X[i, 0] = np.dot(points[i], points[i])
            X[i, 1] = points[i, 0]
            X[i, 2] = points[i, 1]
            X[i, 3] = 1
        m14 = np.linalg.det(X)

        for i in range(4):
            X[i, 0] = np.dot(points[i], points[i])
            X[i, 1] = points[i, 0]
            X[i, 2] = points[i, 1]
            X[i, 3] = points[i, 2]
        m15 = np.linalg.det(X)

        cx = 0.5 * (m12 / m11)
        cy = -0.5 * (m13 / m11)
        cz = 0.5 * (m14 / m11)

        self.center = np.array([cx, cy, cz])
        self.radius = np.sqrt(np.dot(self.center, self.center) - (m15 / m11))

    def from_point_cloud(self, points):
        """
        Least Squares fit.

        Parameters
        ----------
        points: (N, 3) ndarray
        """
        spX = points[:, 0]
        spY = points[:, 1]
        spZ = points[:, 2]

        A = np.zeros((len(spX), 4))
        A[:, 0] = spX * 2
        A[:, 1] = spY * 2
        A[:, 2] = spZ * 2
        A[:, 3] = 1

        #   Assemble the f matrix
        f = np.zeros((len(spX), 1))
        f[:, 0] = (spX * spX) + (spY * spY) + (spZ * spZ)
        center, residules, rank, singval = np.linalg.lstsq(A, f)

        #   solve for the radius
        t = (center[0] * center[0]) + (center[1] * center[1]) + \
            (center[2] * center[2]) + center[3]

        self.center = center[:3].T[0]
        self.radius = np.sqrt(t)

    def get_projections(self, points, only_distances=False):
        vectors = points - self.center
        lengths = np.linalg.norm(vectors, axis=1)
        distances = np.abs(lengths - self.radius)
        if only_distances:
            return distances
        scales = self.radius / lengths
        projections = (scales[:, None] * vectors) + self.center
        return distances, projections
