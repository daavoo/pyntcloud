
"""
HAKUNA MATATA
"""

from .delanuay import Delaunay3D
from .kdtree import KDTree
from .voxelgrid import VoxelGrid

ALL_STRUCTURES = {
    'delanuay3D': Delaunay3D,
    'kdtree': KDTree,
    'voxelgrid': VoxelGrid
}
