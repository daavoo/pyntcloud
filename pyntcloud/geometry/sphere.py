#  HAKUNA MATATA

import numpy as np

class Sphere():

    def __init__(self, center=None, radius=None, normals=False):
        self.center = center
        self.radius= radius
        # for ransac
        self.k = 2 if normals else 4
    
    def from_four_points(self, points):
        # Find the Minors
        X = np.zeros((4,4))

        for i in range(4):
            X[i,0] = points[i,0]
            X[i,1] = points[i,1]
            X[i,2] = points[i,2]
            X[i,3] = 1
        M11 = np.linalg.det(X)

        for i in range(4):
            X[i,0] = np.dot(points[i], points[i])
            X[i,1] = points[i,1]
            X[i,2] = points[i,2]
            X[i,3] = 1
        M12 = np.linalg.det(X)

        for i in range(4):
            X[i,0] = np.dot(points[i], points[i])
            X[i,1] = points[i,0]
            X[i,2] = points[i,2]
            X[i,3] = 1
        M13 = np.linalg.det(X)

        for i in range(4):
            X[i,0] = np.dot(points[i], points[i])
            X[i,1] = points[i,0]
            X[i,2] = points[i,1]
            X[i,3] = 1
        M14 = np.linalg.det(X)

        for i in range(4):
            X[i,0] = np.dot(points[i], points[i])
            X[i,1] = points[i,0]
            X[i,2] = points[i,1]
            X[i,3] = points[i,2]
        M15 = np.linalg.det(X)
        
        
    
    # RANSAC METHODS

    def fit(self, points):
        return

    def get_error(self, points):
        return

    def are_valid(self, points):

        if np.cross(points[1] - points[0], points[2] - points[0]) == 0:
            return False
    
        x = np.ones((4,4))
        x [:-1,:] = points.T
        if np.linalg.det(x) == 0:
            return False

        return True

        
