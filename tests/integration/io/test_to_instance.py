import pytest
import numpy as np
from pyntcloud import PyntCloud

try:
    import pyvista as pv
    SKIP_PYVISTA = False
except:  # noqa: E722
    pv = None
    SKIP_PYVISTA = True

try:
    import open3d as o3d
    SKIP_OPEN3D = False
except:  # noqa: E722
    o3d = None
    SKIP_OPEN3D = True


@pytest.mark.skipif(SKIP_PYVISTA, reason="Requires PyVista")
def test_pyvista_conversion(data_path):
    cloud = PyntCloud.from_file(str(data_path.joinpath("diamond.ply")))
    poly = cloud.to_instance("pyvista", mesh=True)
    assert np.allclose(cloud.xyz, poly.points)
    faces = poly.faces.reshape((-1, 4))[:, 1:]
    assert np.allclose(cloud.mesh.values, faces)


@pytest.mark.skipif(SKIP_OPEN3D, reason="Requires Open3D")
def test_open3d_point_cloud_conversion(data_path):
    cloud = PyntCloud.from_file(str(data_path.joinpath("diamond.ply")))
    point_cloud = cloud.to_instance("open3d", mesh=False)
    assert isinstance(point_cloud, o3d.geometry.PointCloud)
    assert np.allclose(cloud.xyz, point_cloud.points)


@pytest.mark.skipif(SKIP_OPEN3D, reason="Requires Open3D")
def test_open3d_triangle_mesh_conversion(data_path):
    cloud = PyntCloud.from_file(str(data_path.joinpath("diamond.ply")))
    # mesh=True by default
    triangle_mesh = cloud.to_instance("open3d")
    assert isinstance(triangle_mesh, o3d.geometry.TriangleMesh)
    assert np.allclose(cloud.xyz, triangle_mesh.vertices)
    assert np.allclose(cloud.mesh.values, triangle_mesh.triangles)
