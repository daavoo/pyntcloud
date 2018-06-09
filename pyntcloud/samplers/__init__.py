
"""
HAKUNA MATATA
"""

from .points import RandomPointsSampler
from .mesh import RandomMeshSampler
from .voxelgrid import (
    VoxelgridCentersSampler,
    VoxelgridCentroidsSampler,
    VoxelgridNearestSampler,
    VoxelgridHighestSampler
)

ALL_SAMPLERS = {
    # Mesh
    'mesh_random': RandomMeshSampler,
    # Points
    'points_random': RandomPointsSampler,
    # Voxelgrid
    'voxelgrid_centers': VoxelgridCentersSampler,
    'voxelgrid_centroids': VoxelgridCentroidsSampler,
    'voxelgrid_nearest': VoxelgridNearestSampler,
    'voxelgrid_highest': VoxelgridHighestSampler
}
