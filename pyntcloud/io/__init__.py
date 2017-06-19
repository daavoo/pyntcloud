from .ascii import read_ascii, write_ascii
from .las import read_las
from .npz import read_npz, write_npz
from .obj import read_obj, write_obj
from .ply import read_ply, write_ply
from .off import read_off
from .pcd import read_pcd
from .stl import read_stl
FROM = {
    "ASC": read_ascii,
    "CSV": read_ascii,
    "LAS": read_las,
    "NPZ": read_npz,
    "OBJ": read_obj,
    "OFF": read_off,
    "PCD": read_pcd,
    "PLY": read_ply,
    "PTS": read_ascii,
    "STL": read_stl,
    "TXT": read_ascii,
    "XYZ": read_ascii,
}

TO = {
    "ASC": write_ascii,
    "CSV": write_ascii,
    "NPZ": write_npz,
    "OBJ": write_obj,
    "PLY": write_ply,
    "PTS": write_ascii,
    "TXT": write_ascii,
    "XYZ": write_ascii,
}
