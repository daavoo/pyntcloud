
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

ALL_SAMPLING = \
"""
REQUIRE POINTS
--------------
{}

REQUIRE MESH 
------------
{}
""".format(
    *SAMPLE_POINTS,
    *SAMPLE_MESH
)