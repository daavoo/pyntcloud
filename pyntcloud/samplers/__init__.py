
"""
HAKUNA MATATA
"""

from .points import RandomPointsSampler
from .mesh import RandomMeshSampler
from .s_voxelgrid import (
    VoxelgridCenters,
    VoxelgridCentroids,
    VoxelgridNearest
)

ALL_SAMPLERS = {
    # Mesh
    'mesh_random_sampling': RandomMeshSampler,
    # Points
    'points_random_sampling': RandomPointsSampler,
    # Voxelgrid
    'voxelgrid_centers': VoxelgridCenters,
    'voxelgrid_centroids': VoxelgridCentroids,
    'voxelgrid_nearest': VoxelgridNearest
}
