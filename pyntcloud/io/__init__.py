from .ascii import read_ascii
from .las import read_las
from .mat import read_mat
from .npz import read_npz, write_npz
from .obj import read_obj, write_obj
from .ply import read_ply, write_ply
from .off import read_off
from .pcd import read_pcd

FROM = {
    "ASC": read_ascii,
    "LAS": read_las,
    "MAT": read_mat,
    "NPZ": read_npz,
    "OBJ": read_obj,
    "OFF": read_off,
    "PCD": read_pcd,
    "PLY": read_ply,
    "PTS": read_ascii,
    "TXT": read_ascii,
    "XYZ": read_ascii
}

TO = {
    "NPZ": write_npz,
    "OBJ": write_obj,
    "PLY": write_ply
}
