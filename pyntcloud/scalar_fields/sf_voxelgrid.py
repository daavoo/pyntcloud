import numpy as np
from .base import ScalarField

class ScalarField_Voxelgrid(ScalarField):

    def __init__(self, pyntcloud, voxelgrid):
        super().__init__(pyntcloud)
        self.voxelgrid = voxelgrid
    
    def extract_info(self):
        self.voxelgrid = self.pyntcloud.voxelgrids[self.voxelgrid]
    

class VoxelX(ScalarField_Voxelgrid):
    """ Voxel index along x axis.
    """
    def __init__(self, pyntcloud, voxelgrid):
        super().__init__(pyntcloud, voxelgrid)
    
    def compute(self):
        name = "{}({})".format("voxel_x", self.voxelgrid.id)
        self.to_be_added[name] = self.voxelgrid.voxel_x

class VoxelY(ScalarField_Voxelgrid):
    """ Voxel index along y axis.
    """
    def __init__(self, pyntcloud, voxelgrid):
        super().__init__(pyntcloud, voxelgrid)
    
    def compute(self):
        name = "{}({})".format("voxel_y", self.voxelgrid.id)
        self.to_be_added[name] = self.voxelgrid.voxel_y

class VoxelZ(ScalarField_Voxelgrid):
    """ Voxel index along z axis.
    """
    def __init__(self, pyntcloud, voxelgrid):
        super().__init__(pyntcloud, voxelgrid)
    
    def compute(self):
        name = "{}({})".format("voxel_z", self.voxelgrid.id)
        self.to_be_added[name] = self.voxelgrid.voxel_z

class VoxelN(ScalarField_Voxelgrid):
    """ Voxel index in 3D array using 'C' order.
    """
    def __init__(self, pyntcloud, voxelgrid):
        super().__init__(pyntcloud, voxelgrid)
    
    def compute(self):
        name = "{}({})".format("voxel_n", self.voxelgrid.id)
        self.to_be_added[name] = self.voxelgrid.voxel_n
        
class EuclideanClusters(ScalarField_Voxelgrid):
    """ Assing corresponding cluster to each point inside each voxel
    
    """
    def __init__(self, pyntcloud, voxelgrid):
        super().__init__(pyntcloud, voxelgrid)
    
    def compute(self):
        name = "{}({})".format("clusters", self.voxelgrid.id)
        
        to_be_processed = np.zeros(self.voxelgrid.n_voxels, dtype=bool)
        to_be_processed[np.unique(self.voxelgrid.voxel_n)] = True
        
        clusters = np.zeros(self.voxelgrid.voxel_n.shape[0])
        
        C = 0
        while np.any(to_be_processed):
            Q = []
            Q.append(np.random.choice(np.where(to_be_processed)[0]))
            
            for voxel in Q:
                clusters[np.where(self.voxelgrid.voxel_n == voxel)[0]] = C
                to_be_processed[voxel] = False
                neighbors = self.voxelgrid.get_voxel_neighbors(voxel)
                for neighbor in neighbors:
                    if to_be_processed[neighbor]:
                        Q.append(neighbor)
                        to_be_processed[neighbor] = False
            C += 1
            
        self.to_be_added[name] = clusters
