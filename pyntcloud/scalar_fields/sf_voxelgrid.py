
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
