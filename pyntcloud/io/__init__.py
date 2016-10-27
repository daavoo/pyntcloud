
"""
HAKUNA MATATA
"""

from .mat import read_mat
from .npz import read_npz, write_npz
from .obj import read_obj, write_obj
from .pcd import read_pcd, write_pcd
from .ply import read_ply, write_ply

FORMATS_READERS = {
"MAT": read_mat,
"NPZ": read_npz,
"OBJ": read_obj,
"PCD": read_pcd,
"PLY": read_ply
}

FORMATS_WRITERS = {
"NPZ": write_npz,
"OBJ": write_obj,
"PCD": write_pcd,
"PLY": write_ply
}