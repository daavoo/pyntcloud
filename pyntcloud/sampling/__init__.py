
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
    'mesh_random_sampling': RandomMesh,
    # Points
    'points_random_sampling': RandomPoints,
    # Voxelgrid
    'voxelgrid_centers': VoxelgridCenters,
    'voxelgrid_centroids': VoxelgridCentroids,
    'voxelgrid_nearest': VoxelgridNearest
}
