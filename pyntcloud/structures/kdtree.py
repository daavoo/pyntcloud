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
        
        """ Compute the eigen decomposition of each point's neighbourhood

        Parameters
        ----------

        k: int
            The number of neighbours that will be used to query the kdtree.
        indices: ndarray
            Default: None
            (N, k) ndarray indicating the index of the k neighbours associated
            to each of the N points in self.data.
            If indices are supplied the kdtree won't be queried and k parameter
            will be ignored.
        return_eigenvectors: bool
            Default: False
            Indicates if eigenvectors are also returned or not.
        
        Returns
        -------
        eig_val1, eig_val2, eig_val3: ndarray
            (N,) ndarray each one holding the eigenvalues sorted in descending order.
        
        eig_vec1, eig_vec3, eig_vec3: ndarray
            Only if return_eigenvectors == True.
            (N,3) ndarray holding the vector associated to corresponding eigenvalue.
        """

        if indices is None:
            print("Querying KDTREE...")
            d, i = self.query(self.data, k=k, n_jobs=-1)
        else:
            i = indices

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
        if return_eigenvectors:
            eig_vec1 = eigenvectors[idx_trick, :, sort[:,2]]
            eig_vec2 = eigenvectors[idx_trick, :, sort[:,1]]
            eig_vec3 = eigenvectors[idx_trick, :, sort[:,0]] 
            return eig_val1, eig_val2, eig_val3, eig_vec1, eig_vec2, eig_vec3 
        else:
            return eig_val1, eig_val2, eig_val3
