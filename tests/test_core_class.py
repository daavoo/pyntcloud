import os
import pytest
import numpy as np
import pandas as pd
from shutil import rmtree
from pyntcloud import PyntCloud

path = os.path.abspath(os.path.dirname(__file__))


def test_points():
    """PyntCloud.points.

    - Points must be a pandas DataFrame
    - DataFrame must have at least "x", "y" and "z" named columns
    - When PyntCloud.points is re-assigned all structures must be removed

    """
    points = np.random.rand(10, 3)

    # not dataframe
    with pytest.raises(TypeError):
        PyntCloud(points)

    points = pd.DataFrame(points)

    # not x, y, z
    with pytest.raises(ValueError):
        PyntCloud(points)

    points = pd.DataFrame(points.values, columns=["x", "y", "z"])

    assert PyntCloud(points)

    cloud = PyntCloud(points)

    cloud.add_structure("voxelgrid")

    assert len(cloud.structures) == 1

    # dummy filter
    x_above_05 = cloud.points["x"] > 0.5
    cloud.points = cloud.points[x_above_05]

    assert len(cloud.structures) == 0


def test_repr():
    """PyntCloud.__repr__.

    - When custom attributes are added, __repr__ must show its name and type

    """
    points = np.random.rand(10, 3)
    points = pd.DataFrame(points, columns=["x", "y", "z"])
    cloud = PyntCloud(points)

    # some dummy attribute
    important_dict = {"black": "Carl", "white": "Lenny"}
    cloud.important_information = important_dict

    reprstring = cloud.__repr__()
    reprstring = reprstring.split("\n")

    assert reprstring[-2].strip() == "important_information: <class 'dict'>"


def test_split_on():
    """PyntCloud.split_on.

    - Raise KeyError on invalid scalar field
    - Raise ValueError on invalid save_format
    - and_return should return list of PyntClouds
    - Implicitily check save_path is working

    """
    cloud = PyntCloud.from_file(path + "/data/mnist.npz")
    vg_id = cloud.add_structure("voxelgrid", x_y_z=[2, 2, 2])

    voxel_n = cloud.add_scalar_field("voxel_n", voxelgrid=vg_id)

    with pytest.raises(KeyError):
        cloud.split_on("bad_sf")

    with pytest.raises(ValueError):
        cloud.split_on(voxel_n, save_format="bad_format")

    output = cloud.split_on(voxel_n, save_path="tmp_out")

    assert output is None

    output = cloud.split_on(voxel_n, and_return=True, save_path="tmp_out")

    assert len(output) == 8

    rmtree("tmp_out")
