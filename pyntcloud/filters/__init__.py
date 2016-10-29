
"""
HAKUNA MATATA
"""

from .filters import *

F_NEIGHBOURHOOD = {
"ROR": ('r', radious_outlier_removal),
"SOR": ('z_max', statistical_outlier_removal)
}
F_XYZ = {
"BB": (["min_x", "max_x", "min_y", "max_y", "min_z", "max_z"], bounding_box),
"random": ('size', random)
}

ALL_FILTERS = "  ".join(F_NEIGHBOURHOOD.keys()) + "  " + \
        "  ".join(F_XYZ.keys())