#  HAKUNA MATATA

"""
KDTree Class extending cKDTree
"""


from scipy.spatial import cKDTree

class KDTree(cKDTree):
    # TODO instead of extend cKDTree make this class a wrapper
    # around different KDTree implementations: scipy, flann, etc.

    def __init__(self, points, leafsize=16):
        self.id = "K {}".format( self.leafsize)
        super().__init__(points, leafsize=leafsize)
        


    def eigen_decomposition(self, **kwargs):
        print("Querying KDTREE...")

        valid_args = {key: kwargs[key] for key in kwargs if key in ['k', 'eps', 'p', 'distance_upper_bound']} 
            if 'k' not in valid_args:
                valid_args["k"] = 2
        d, i = kdtree.query(kdtree.data, k=k, n_jobs=-1, **valid_args)
        # discard self neighbour with [:,1:]
        distances = d[:,1:]
        indices = i[:,1:]

        print("Computing eigen decomposition...")

        neighbours = self.points[indices]
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
