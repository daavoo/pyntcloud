
"""
HAKUNA MATATA
"""

from .filters import *

F_NEIGHBOURHOOD = {
"ROR": ('r', radious_outlier_removal),
"SOR": ('z_max', statistical_outlier_removal)
}