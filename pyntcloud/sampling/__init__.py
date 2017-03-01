
"""
HAKUNA MATATA
"""

from .s_points import random_sampling
from .s_mesh import mesh_sampling
from .s_voxelgrid import (
    voxelgrid_centers,
    voxelgrid_centroids,
    voxelgrid_nearest
)

S_POINTS = {
    'random_sampling': random_sampling
} 

S_MESH = {
    'mesh_sampling': random_sampling
} 

S_VOXELGRID = {
    'voxelgrid_centers': voxelgrid_centers,
    'voxelgrid_centroids': voxelgrid_centroids,
    'voxelgrid_nearest': voxelgrid_nearest
}

ALL_SAMPLING = \
"""
REQUIRE POINTS
--------------
{}

REQUIRE MESH 
------------
{}

REQUIRE VOXLEGRID 
------------
{}
{}
{}
""".format(
    *SAMPLE_POINTS,
    *SAMPLE_MESH,
    *SAMPLE_VOXELGRID
)