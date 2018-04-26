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
def pyntcloud_with_kdtree_and_kdtree_id(simple_pyntcloud):
    kdtree_id = simple_pyntcloud.add_structure("kdtree")
    return simple_pyntcloud, kdtree_id


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
@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def pyntcloud_with_voxelgrid_and_voxelgrid_id(pyntcloud_with_rgb_and_normals):
    voxelgrid_id = pyntcloud_with_rgb_and_normals.add_structure("voxelgrid", x_y_z=[4, 4, 4])
    return pyntcloud_with_rgb_and_normals, voxelgrid_id


@pytest.fixture()
def pyntcloud_with_clusters_and_voxelgrid_id():
    xyz = np.random.rand(10, 3)
    xyz[:5, :] += 10

    cloud = PyntCloud(pd.DataFrame(
        data=xyz,
        columns=["x", "y", "z"]))

    voxelgrid_id = cloud.add_structure("voxelgrid", sizes=[0.5, 0.5, 0.5])

    return cloud, voxelgrid_id


@pytest.fixture()
@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def pyntcloud_with_rgb_and_normals_k_neighbors(pyntcloud_with_rgb_and_normals):
    return pyntcloud_with_rgb_and_normals.get_neighbors(k=3)


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
            [0., 0., 0.],
            [1., 1., 0.],
            [2., 2., 0.],
            [1., 2., 0.],
            [0.1, 0.2, 0.3]], dtype=np.float32),
        columns=["x", "y", "z"]))


@pytest.fixture()
def sphere_pyntcloud():
    return PyntCloud(pd.DataFrame(
        data=np.array([
            [-1., 0., 0.],
            [0., 0., 1.],
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.2]], dtype=np.float32),
        columns=["x", "y", "z"]))


@pytest.fixture()
def plane_k_neighbors():
    return np.array([
        [4, 1],
        [3, 4],
        [3, 1],
        [1, 2],
        [0, 1]])


@pytest.fixture()
def pyntcloud_and_eigenvalues():
    cloud = PyntCloud(pd.DataFrame(
        data={
            "x": np.array([0, 0, 1, -1, 0, 0], dtype=np.float32),
            "y": np.array([0, 1, 0, 0, -1, 0], dtype=np.float32),
            "z": np.array([0, 0, 0, 0, 0, 2], dtype=np.float32)
        }))

    k_neighbors = cloud.get_neighbors(k=4)

    ev = cloud.add_scalar_field("eigen_values", k_neighbors=k_neighbors)

    return cloud, ev
