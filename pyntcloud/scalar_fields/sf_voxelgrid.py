

def voxel_x(voxelgrid):
    """ Voxel index along x axis.
    """
    return [voxelgrid.voxel_x]

def voxel_y(voxelgrid):
    """ Voxel index along y axis.
    """
    return [voxelgrid.voxel_y]

def voxel_z(voxelgrid):
    """ Voxel index along z axis.
    """
    return [voxelgrid.voxel_z]

def voxel_n(voxelgrid):
    """ Voxel index in 3D array using 'C' order.
    """
    return [voxelgrid.voxel_n] 