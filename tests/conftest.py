import pytest

import numpy as np
import pandas as pd

from pyntcloud import PyntCloud


@pytest.fixture()
def xyz():
    return np.array([
        [0. , 0. , 0. ],
        [0.1, 0.1, 0.1],
        [0.2, 0.2, 0.2],
        [0.5, 0.5, 0.5],
        [0.9, 0.9, 0.9],
        [1. , 1. , 1. ]], dtype=np.float32)


@pytest.fixture()
@pytest.mark.usefixtures("xyz")
def simple_pyntcloud(xyz):
    return PyntCloud(pd.DataFrame(
        data=xyz,
        columns=["x", "y", "z"]))


@pytest.fixture()
@pytest.mark.usefixtures("simple_pyntcloud")
def pyntcloud_with_kdtree(simple_pyntcloud):
    simple_pyntcloud.add_structure("kdtree")
    return simple_pyntcloud


@pytest.fixture()
def pyntcloud_with_rgb_and_normals():
    return PyntCloud(points=pd.DataFrame(
        data={
            "x": np.random.rand(1000).astype(np.float32),
            "y": np.random.rand(1000).astype(np.float32),
            "z": np.random.rand(1000).astype(np.float32),
            "red": np.random.randint(0, 255, size=1000, dtype=np.uint8),
            "green": np.random.randint(0, 255, size=1000, dtype=np.uint8),
            "blue": np.random.randint(0, 255, size=1000, dtype=np.uint8),
            "nx": np.random.rand(1000).astype(np.float32),
            "ny": np.random.rand(1000).astype(np.float32),
            "nz": np.random.rand(1000).astype(np.float32)}))

@pytest.fixture()
def diamond():
    points = pd.DataFrame(
        data={
            "x": np.array([0.5, 0., 0.5, 1., 0.5, 0.5], dtype=np.float32),
            "y": np.array([0., 0.5, 0.5, 0.5, 1., 0.5], dtype=np.float32),
            "z": np.array([0.5, 0.5, 0., 0.5, 0.5, 1.], dtype=np.float32),
            "red": np.array([255, 255, 0, 255, 255, 0], dtype=np.uint8),
            "green": np.array([0, 0, 255, 0, 0, 0], dtype=np.uint8),
            "blue": np.array([0, 0, 0, 0, 0, 255], dtype=np.uint8),
            "nx": np.array([0., -1., 0., 1., 0., 0.], dtype=np.float32),
            "ny": np.array([-1., 0., 0., 0., 1., 0.], dtype=np.float32),
            "nz": np.array([0., 0., -1., 0., 0., 1.], dtype=np.float32)
        })

    vertices = np.array([
        [0, 1, 2],
        [0, 3, 2],
        [3, 4, 2],
        [4, 1, 2],
        [0, 1, 5],
        [0, 3, 5],
        [3, 4, 5],
        [4, 1, 5]])

    mesh = pd.DataFrame(
        data=vertices,
        columns=["v1", "v2", "v3"])

    return PyntCloud(points=points, mesh=mesh)


@pytest.fixture()
def plane_pyntcloud():
    return PyntCloud(pd.DataFrame(
        data=np.array([
            [0. , 0. , 0. ],
            [1. , 1. , 0. ],
            [2. , 2. , 0. ],
            [1. , 2. , 0. ],
            [0.1, 0.2, 0.3]], dtype=np.float32)),
        columns=["x", "y", "z"])

