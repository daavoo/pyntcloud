import numpy as np
import pandas as pd
from .base import GeometryModel

class Ellipsoid(GeometryModel):

    def __init__(self, center=None, radii=None, evecs=None, evals=None):
        self.center = center
        self.radii = radii
        self.evecs = evecs
        self.evals = evals

    def from_k_points(self, points):
        '''
        Execute the ellipsoid least squares fit on a subset using 
        k point of the point cluoud. 
        To fit the ellispod at leasn k=11 non complanar points are required.
        '''
        
        self.from_point_cloud(points)


    def from_point_cloud(self, points):
        """
        Least Squares fit.
        The code for the fit is from
        https://github.com/aleksandrbazhin/ellipsoid_fit_python

        Parameters
        ----------
        points: (N, 3) ndarray
        """
        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]
        
        D = np.array([x * x + y * y - 2 * z * z,
                 x * x + z * z - 2 * y * y,
                 2 * x * y,
                 2 * x * z,
                 2 * y * z,
                 2 * x,
                 2 * y,
                 2 * z,
                 1 - 0 * x])
        d2 = np.array(x * x + y * y + z * z).T # rhs for LLSQ
        
        u = np.linalg.solve(D.dot(D.T), D.dot(d2))
        a = np.array([u[0] + 1 * u[1] - 1])
        b = np.array([u[0] - 2 * u[1] - 1])
        c = np.array([u[1] - 2 * u[0] - 1])
        v = np.concatenate([a, b, c, u[2:]], axis=0).flatten()
        A = np.array([[v[0], v[3], v[4], v[6]],
                      [v[3], v[1], v[5], v[7]],
                      [v[4], v[5], v[2], v[8]],
                      [v[6], v[7], v[8], v[9]]])
        
        self.center = np.linalg.solve(- A[:3, :3], v[6:9])
        
        translation_matrix = np.eye(4)
        translation_matrix[3, :3] = self.center.T

        R = translation_matrix.dot(A).dot(translation_matrix.T)
        self.A = R
        # get the eigenvalues and the RIGHT eigenvectors
        self.evals, self.evecs = np.linalg.eig(R[:3, :3] / -R[3, 3])
        # convert the ritght eigenvectors to the LEFT eigenvecors
        self.evecs = self.evecs.T

        self.radii = np.sqrt(1. / np.abs(self.evals))
        self.radii *= np.sign(self.evals)
        

    def get_projections(self, points, only_distances=False):
        '''
        Compute the distances between each point of the point cloud and the ellipsoid surface.
        If only_distances=False, it will also project the points onto the ellipsoid surface.
        '''
        
        # compute the vector jointing the center of the ellipsoid
        # and the objective point. Compute also its lenght
        vectors = points - self.center
        lenghts = np.linalg.norm(vectors, axis=-1)
        
        # to find the distance between the point and the surface, I have to 
        # subtract the distance between the origin and the intersection point between 
        # the ellipsoid surface and the line connecting the point and the center
        # To find this point, I will solve the system composed by the line and the 
        # ellipsoid equation.
        # The ellipsoid equation is obtained from the general quadric equation in non-homoegeous corrdinates.s
        # The system is solved by substituion, computing the y coordinate that is used 
        # to found the other two.
        # The whole procedure is on the reference system centered on the ellipsoid center
        # The whole solution is computed in a reference system with origin at the ellipsoid center.

        centered_points = points - self.center
        
        # define some scale quantity to compute x, z coordinetes out of the y one
        N_x = centered_points[:, 0] / centered_points[:, 1]
        N_z = centered_points[:, 2] / centered_points[:, 1]
        
        # now write the term of the second order equation derived respect to y
        
        alpha_x = (self.A[0, 0] * N_x + 2 * self.A[0, 1]) * N_x
        alpha_z = (self.A[2, 2] * N_z + 2 * self.A[1, 2]) * N_z
        alpha_y = 2 * self.A[0, 2] * N_x * N_z + self.A[1, 1]
        alpha = alpha_x + alpha_z + alpha_y
        
        beta = 2 * (self.A[0, 3] * N_x + self.A[2, 3] * N_z + self.A[1, 3])
        gamma = self.A[3, 3]
        
        # The system has two solutions, I will pick up the positive one
        yi = (- beta + np.sqrt(beta ** 2 - 4 * alpha * gamma)) / (2 * alpha)        
        xi = N_x * yi
        zi = N_z * yi
        
        # organize point coordinates into a single matrix
        res_points = np.concatenate([xi[..., np.newaxis], yi[..., np.newaxis], zi[..., np.newaxis]], axis=-1)

        # and so I can compute the required distance (remenìmber that the system is centered at the ellipsoid center)
        generalized_radii = np.linalg.norm(res_points, axis=1)
        
        # so finally the distance between each point of the point cloud and the ellipsoid
        # surface reads:
        distances = np.abs(lenghts - generalized_radii)
        
        if only_distances:
            return distances
        
        scales = generalized_radii / lengths
        projections = (scales[:, None] * vectors) + self.center
        
        return distances, projections