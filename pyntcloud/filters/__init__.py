
"""
HAKUNA MATATA
"""

from .filters import *

F_KDTREE = {
        "ROR": radious_outlier_removal,
        "SOR": statistical_outlier_removal
}

F_XYZ = {
        "BBOX": bounding_box
}

ALL_FILTERS = "".join([" {}"] * 2).format(
    list(F_KDTREE),
    list(F_XYZ)
)