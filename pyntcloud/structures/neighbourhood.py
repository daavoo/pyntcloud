#  HAKUNA MATATA

"""
Neighbourhood Class
"""

import numpy as np
from scipy.stats import zscore

class Neighbourhood(object):
    
    def __init__(self, kdtree, k, eigen=True, **kwargs):
        """
        Parameters
        ----------         
        """
        print("Querying KDTREE...")
        d, i = kdtree.query(kdtree.data, k=k, n_jobs=-1, **kwargs)
        # discard self neighbour with [:,1:]
        self.points = kdtree.data
        self.distances = d[:,1:]
        self.indices = i[:,1:]
        self.k = k - 1
        self.id = "{}-{}".format(kdtree.id, self.k)
        
        if eigen:
            print("Computing eigen decomposition...")
            self.eigen_decomposition()
    
    def eigen_decomposition(self):
        
        neighbours = self.points[self.indices]

        diffs = neighbours - neighbours.mean(1,keepdims=True)
    
        cov_3D = np.einsum('ijk,ijl->ikl',diffs,diffs) / neighbours.shape[1]

        eigenvalues, eigenvectors = np.linalg.eig(cov_3D)

        sort = eigenvalues.argsort()
        # range from 0-shape[0] to allow indexing along axis 1 and 2
        idx_trick = range(eigenvalues.shape[0])

        self.eig_val1 = eigenvalues[idx_trick, sort[:,2]]
        self.eig_val2 = eigenvalues[idx_trick, sort[:,1]]
        self.eig_val3 = eigenvalues[idx_trick, sort[:,0]]

        self.eig_vec1 = eigenvectors[idx_trick, :, sort[:,2]]
        self.eig_vec2 = eigenvectors[idx_trick, :, sort[:,1]]
        self.eig_vec3 = eigenvectors[idx_trick, :, sort[:,0]]        

