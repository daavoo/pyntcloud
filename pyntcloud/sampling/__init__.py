
"""
HAKUNA MATATA
"""

from .s_points import RandomPoints
from .s_mesh import RandomMesh
from .s_voxelgrid import (
    VoxelgridCenters,
    VoxelgridCentroids,
    VoxelgridNearest
)

ALL_SAMPLING = {
    # Mesh            
    'random_mesh': RandomMesh, 
    # Points
    'random_points' : RandomPoints,    
    # Voxelgrid
    'voxelgrid_centers' : VoxelgridCenters,
    'voxelgrid_centroids' : VoxelgridCentroids,
    'voxelgrid_nearest' : VoxelgridNearest
}
