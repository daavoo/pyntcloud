import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, depth_first_order

from .base import ScalarField
from ..utils.array import cov3D


class ScalarField_KNeighbors(ScalarField):
    """
    Parameters
    ----------
    k_neighbors: ndarray
        (N, k, 3) The k neighbours associated to each of the N points.
    """

    def __init__(self, pyntcloud, k_neighbors):
        super().__init__(pyntcloud)
        self.k_neighbors_idx = k_neighbors

    def extract_info(self):
        self.k_neighbors = self.pyntcloud.xyz[self.k_neighbors_idx]


class EigenValues(ScalarField_KNeighbors):
    """Compute the eigen values of each point's neighbourhood.
    """
    def compute(self):
        cov = cov3D(self.k_neighbors)
        eigenvalues = np.linalg.eigvals(cov)
        sort = eigenvalues.argsort()

        # range from 0-shape[0] to allow indexing along axis 1 and 2
        idx_trick = range(eigenvalues.shape[0])

        e1 = eigenvalues[idx_trick, sort[:, 2]]
        e2 = eigenvalues[idx_trick, sort[:, 1]]
        e3 = eigenvalues[idx_trick, sort[:, 0]]

        k = self.k_neighbors.shape[1]
        self.to_be_added["e1({})".format(k)] = e1
        self.to_be_added["e2({})".format(k)] = e2
        self.to_be_added["e3({})".format(k)] = e3


class EigenDecomposition(ScalarField_KNeighbors):
    """Compute the eigen decomposition of each point's neighbourhood.
    """
    def compute(self):
        cov = cov3D(self.k_neighbors)
        eigenvalues, eigenvectors = np.linalg.eig(cov)
        sort = eigenvalues.argsort()

        # range from 0-shape[0] to allow indexing along axis 1 and 2
        idx_trick = range(eigenvalues.shape[0])

        e1 = eigenvalues[idx_trick, sort[:, 2]]
        e2 = eigenvalues[idx_trick, sort[:, 1]]
        e3 = eigenvalues[idx_trick, sort[:, 0]]

        k = self.k_neighbors.shape[1]
        self.to_be_added["e1({})".format(k)] = e1
        self.to_be_added["e2({})".format(k)] = e2
        self.to_be_added["e3({})".format(k)] = e3

        ev1 = eigenvectors[idx_trick, :, sort[:, 2]]
        ev2 = eigenvectors[idx_trick, :, sort[:, 1]]
        ev3 = eigenvectors[idx_trick, :, sort[:, 0]]

        self.to_be_added["ev1({})".format(k)] = ev1.tolist()
        self.to_be_added["ev2({})".format(k)] = ev2.tolist()
        self.to_be_added["ev3({})".format(k)] = ev3.tolist()


class Normals(ScalarField_KNeighbors):
    """Compute normals using SVD and refine orientation with Riemanian Graph.
    """
    def compute(self):
        cov = cov3D(self.k_neighbors)
        u, s, v = np.linalg.svd(cov)

        normals = u[:, :, -1]

        # Orient normals as in "Surface Reconstruction from Unorganized Points"

        max_z = self.pyntcloud.xyz.argmax(0)[-1]
        if normals[max_z, 2] < 0:
            normals[max_z] = -normals[max_z]
        
        # Dot product between each point's normal and the normals of it's neighbours
        dot3D = 1 - abs(np.einsum("ij, ikj -> ik",
                                  normals,
                                  normals[self.k_neighbors_idx]))

        n = self.pyntcloud.xyz.shape[0]
        graph = np.zeros((n, n), dtype=np.float32)
        for i in range(n):
            graph[i, self.k_neighbors_idx[i]] = dot3D[i]

        MST = minimum_spanning_tree(csr_matrix(graph))
        DFO = depth_first_order(MST, max_z,
                                directed=False,
                                return_predecessors=False)
        """
        for i in range(1, len(DFO)):
            n1 = normals[DFO[i - 1]]
            n2 = normals[DFO[i]]
            if np.dot(n1, n2) < 0:
                normals[DFO[i]] *= -1
        """
        nx = normals[:, 0]
        ny = normals[:, 1]
        nz = normals[:, 2]

        k = self.k_neighbors.shape[1]
        self.to_be_added["nx({})".format(k)] = nx
        self.to_be_added["ny({})".format(k)] = ny
        self.to_be_added["nz({})".format(k)] = nz
