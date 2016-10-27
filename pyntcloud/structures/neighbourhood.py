#  HAKUNA MATATA

"""
Neighbourhood Class
"""

import numpy as np

class Neighbourhood(object):
    
    def __init__(self, kdtree, k, **kwargs):
        """
        Parameters
        ----------         
        """
        self.points = kdtree.data
        self.k = k
        self.id = "{}-{}".format(kdtree.id, self.k)

        d, i = kdtree.query(kdtree.data, k=k, n_jobs=-1, **kwargs)
        # discard self neighbour with [:,1:]
        self.distances = d[:,1:]
        self.indices = i[:,1:]
    
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

        

