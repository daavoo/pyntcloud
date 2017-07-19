
"""
HAKUNA MATATA
"""
from .convex_hull import ConvexHull
from .delanuay import Delaunay3D
from .kdtree import KDTree
from .voxelgrid import VoxelGrid

ALL_STRUCTURES = {
    'convex_hull': ConvexHull,
    'delanuay3D': Delaunay3D,
    'kdtree': KDTree,
    'voxelgrid': VoxelGrid
}
