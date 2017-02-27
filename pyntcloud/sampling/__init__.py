
"""
HAKUNA MATATA
"""

from .sampling import *

SAMPLE_POINTS = {
    'random_sampling': random_sampling
} 

SAMPLE_MESH = {
    'mesh_sampling': random_sampling
} 

SAMPLE_VOXELGRID = {
    'voxelgrid_centers': voxelgrid_centers,
    'voxelgrid_centroids': voxelgrid_centroids
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

""".format(
    *SAMPLE_POINTS,
    *SAMPLE_MESH,
    *SAMPLE_VOXELGRID
)