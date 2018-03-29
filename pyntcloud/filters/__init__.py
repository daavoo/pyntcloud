
"""
HAKUNA MATATA
"""

from .kdtree import (
    RadiusOutlierRemovalFilter,
    StatisticalOutlierRemovalFilter,

)
from .f_xyz import BoundingBox

ALL_FILTERS = {
    # XYZ
    "BBOX": BoundingBox,
    # KDTree
    "ROR": RadiusOutlierRemovalFilter,
    "SOR": StatisticalOutlierRemovalFilter
}
