import pytest
import numpy as np
from pyntcloud import PyntCloud

try:
    import pyvista as pv
    SKIP_PYVISTA = False
except:
    pv = None
    SKIP_PYVISTA = True

try:
    import open3d as o3d
    SKIP_OPEN3D = False
except:
    o3d = None
    SKIP_OPEN3D = True


@pytest.mark.skipif(SKIP_PYVISTA, reason="Requires PyVista")
def test_pyvista_conversion(data_path):
    poly = pv.read(str(data_path.joinpath("diamond.ply")))
    pc = PyntCloud.from_instance("pyvista", poly)
    assert np.allclose(pc.points[['x', 'y', 'z']].values, poly.points)


@pytest.mark.skipif(SKIP_PYVISTA, reason="Requires PyVista")
def test_pyvista_normals_are_handled():
    poly = pv.Sphere()
    pc = PyntCloud.from_instance("pyvista", poly)
    assert all(x in pc.points.columns for x in ["nx", "ny", "nz"])


@pytest.mark.skipif(SKIP_PYVISTA, reason="Requires PyVista")
def test_pyvista_multicomponent_scalars_are_splitted():
    poly = pv.Sphere()
    poly.point_arrays["foo"] = np.zeros_like(poly.points)
    pc = PyntCloud.from_instance("pyvista", poly)
    assert all(x in pc.points.columns for x in ["foo_0", "foo_1", "foo_2"])


@pytest.mark.skipif(SKIP_PYVISTA, reason="Requires PyVista")
def test_pyvista_rgb_is_handled():
    """ Serves as regression test for old `in` behaviour that could cause a subtle bug
    if poin_arrays contain a field with `name in "RGB"`
    """
    poly = pv.Sphere()
    poly.point_arrays["RG"] = np.zeros_like(poly.points)[:, :2]
    pc = PyntCloud.from_instance("pyvista", poly)
    assert all(x in pc.points.columns for x in ["RG_0", "RG_1"])


@pytest.mark.skipif(SKIP_OPEN3D, reason="Requires Open3D")
def test_open3d_point_cloud(data_path):
    point_cloud = o3d.io.read_point_cloud(str(data_path.joinpath("diamond.ply")))
    cloud = PyntCloud.from_instance("open3d", point_cloud)
    assert np.allclose(cloud.xyz, np.asarray(point_cloud.points))
    assert {'red', 'green', 'blue'}.issubset(cloud.points.columns)
    assert np.allclose(cloud.points[['red', 'green', 'blue']].values / 255., np.asarray(point_cloud.colors))

    assert {'nx', 'ny', 'nz'}.issubset(cloud.points.columns)
    assert np.allclose(cloud.points[['nx', 'ny', 'nz']].values,  np.asarray(point_cloud.normals))


@pytest.mark.skipif(SKIP_OPEN3D, reason="Requires Open3D")
def test_open3d_triangle_mesh(data_path):
    triangle_mesh = o3d.io.read_triangle_mesh(str(data_path.joinpath("diamond.ply")))
    cloud = PyntCloud.from_instance("open3d", triangle_mesh)
    assert cloud.mesh is not None
    assert np.allclose(cloud.mesh.values, triangle_mesh.triangles)

    assert np.allclose(cloud.xyz, triangle_mesh.vertices)

    assert {'red', 'green', 'blue'}.issubset(cloud.points.columns)
    assert np.allclose(cloud.points[['red', 'green', 'blue']].values / 255., triangle_mesh.vertex_colors)

    assert {'nx', 'ny', 'nz'}.issubset(cloud.points.columns)
    assert np.allclose(cloud.points[['nx', 'ny', 'nz']].values,  triangle_mesh.vertex_normals)
