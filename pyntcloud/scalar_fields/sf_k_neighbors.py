import numpy as np

def eigen_decomposition(k_neighbors, return_eigenvectors=True):
        """ Compute the eigen decomposition of each point's neighbourhood

        Parameters
        ----------
        k_neighbors: ndarray
            (N, k, 3) The k neighbours associated to each of the N points.
        
        Returns
        -------
        eig_val1, eig_val2, eig_val3: ndarray
            (N,) ndarray each one holding the eigenvalues sorted in descending order.
        
        eig_vec1, eig_vec3, eig_vec3: ndarray
            Only if return_eigenvectors == True.
            (N,3) ndarray holding the vector associated to corresponding eigenvalue.
        """

        diffs = k_neighbors - k_neighbors.mean(1,keepdims=True)
        cov_3D = np.einsum('ijk,ijl->ikl', diffs, diffs) / k_neighbors.shape[1]

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

def eigen_values(k_neighbors):
    return eigen_decomposition(k_neighbors, return_eigenvectors=False)