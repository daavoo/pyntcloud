
"""
HAKUNA MATATA
"""

from .f_kdtree import (
        statistical_outlier_removal,
        radious_outlier_removal
)

from .f_xyz import bounding_box

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
{}
""".format(
    *F_XYZ,
    *F_KDTREE
)