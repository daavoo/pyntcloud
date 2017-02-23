
"""
HAKUNA MATATA
"""

from .filters import *

F_XYZ = {
        "BBOX": bounding_box
}

F_KDTREE = {
        "ROR": radious_outlier_removal,
        "SOR": statistical_outlier_removal
}

ALL_FILTERS = \
"""
REQUIRE POINTS
--------------
{}

REQUIRE KDTREE 
--------------
{}
""".format(
    *F_XYZ,
    *F_KDTREE
)