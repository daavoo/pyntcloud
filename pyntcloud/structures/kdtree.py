#  HAKUNA MATATA

"""
KDTree Class extending cKDTree
"""

import numpy as np
from scipy.spatial import cKDTree


class KDTree(cKDTree):
    # TODO instead of extend cKDTree make this class a wrapper
    # around different KDTree implementations: scipy, flann, etc.

    def __init__(self, points, leafsize=16):
        self.id = "K({})".format(leafsize)
        super().__init__(points, leafsize=leafsize)
        

    def eigen_decomposition(self, k):
        print("Querying KDTREE...")
        d, i = self.query(self.data, k=k, n_jobs=-1)
        print("Computing eigen decomposition...")
        # discard self neighbour with [:,1:]
        neighbours = self.data[i[:,1:]]
        diffs = neighbours - neighbours.mean(1,keepdims=True)
        cov_3D = np.einsum('ijk,ijl->ikl', diffs, diffs) / neighbours.shape[1]
        eigenvalues, eigenvectors = np.linalg.eig(cov_3D)
        sort = eigenvalues.argsort()

        # range from 0-shape[0] to allow indexing along axis 1 and 2
        idx_trick = range(eigenvalues.shape[0])
        eig_val1 = eigenvalues[idx_trick, sort[:,2]]
        eig_val2 = eigenvalues[idx_trick, sort[:,1]]
        eig_val3 = eigenvalues[idx_trick, sort[:,0]]
        eig_vec1 = eigenvectors[idx_trick, :, sort[:,2]]
        eig_vec2 = eigenvectors[idx_trick, :, sort[:,1]]
        eig_vec3 = eigenvectors[idx_trick, :, sort[:,0]] 

        return eig_val1, eig_val2, eig_val3, eig_vec1, eig_vec2, eig_vec3 
