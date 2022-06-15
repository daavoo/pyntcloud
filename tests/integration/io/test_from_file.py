import pytest

import numpy as np

from pyntcloud import PyntCloud


def assert_points_xyz(data):
    assert np.isclose(data.points['x'][0], 0.5)
    assert np.isclose(data.points['y'][0], 0)
    assert np.isclose(data.points['z'][0], 0.5)

    assert str(data.points["x"].dtype) == 'float32'
    assert str(data.points["y"].dtype) == 'float32'
    assert str(data.points["z"].dtype) == 'float32'


def assert_points_xyz_for_las(data):
    assert np.isclose(data.points['x'][0], 0.5)
    assert np.isclose(data.points['y'][0], 0)
    assert np.isclose(data.points['z'][0], 0.5)

    assert str(data.points["x"].dtype) == 'float64'
    assert str(data.points["y"].dtype) == 'float64'
    assert str(data.points["z"].dtype) == 'float64'


def assert_points_color(data):
    assert data.points['red'][0] == 255
    assert data.points['green'][0] == 0
    assert data.points['blue'][0] == 0

    assert str(data.points['red'].dtype) == 'uint8'
    assert str(data.points['green'].dtype) == 'uint8'
    assert str(data.points['blue'].dtype) == 'uint8'


def assert_mesh(data):
    assert data.mesh["v1"][0] == 0
    assert data.mesh["v2"][0] == 1
    assert data.mesh["v3"][0] == 2

    assert str(data.mesh['v1'].dtype) == 'int32'
    assert str(data.mesh['v2'].dtype) == 'int32'
    assert str(data.mesh['v3'].dtype) == 'int32'


@pytest.mark.parametrize("extension,color,mesh,comments", [
    (".ply", True, True, False),
    ("_ascii.ply", True, True, True),
    ("_ascii_vertex_index.ply", True, True, True),
    (".npz", True, True, False),
    (".obj", False, True, False),
    (".off", False, False, False),
    ("_color.off", True, False, False),
    (".bin", False, False, False),
    (".las", True, False, False),
    (".laz", True, False, False)
])
def test_from_file(data_path, extension, color, mesh, comments):
    if extension == ".laz":
        pytest.xfail("TODO: Review laz decompression error")
    cloud = PyntCloud.from_file(str(data_path / "diamond{}".format(extension)))

    if extension == ".las":
        assert_points_xyz_for_las(cloud)
    else:
        assert_points_xyz(cloud)

    if color:
        assert_points_color(cloud)
    if mesh:
        assert_mesh(cloud)
    if comments:
        assert cloud.comments == ["PyntCloud is cool"]


def test_obj_issue_221(data_path):
    """ Regression test https://github.com/daavoo/pyntcloud/issues/221
    """
    cloud = PyntCloud.from_file(str(data_path / "obj_issue_221.obj"))

    assert (len(cloud.xyz)) == 42
    assert (len(cloud.mesh)) == 88


def test_obj_issue_226(data_path):
    """ Regression test https://github.com/daavoo/pyntcloud/issues/226
    """
    cloud = PyntCloud.from_file(str(data_path / "obj_issue_226.obj"))

    assert "w" in cloud.points.columns


def test_obj_issue_vn(data_path):
    """
    Fix type issue in pyntcloud/io/obj.py.
    A float is passed to range() instead of an integer.
    for i in range(f[0].count("/") / 2):
    TypeError: 'float' object cannot be interpreted as an integer
    """
    cloud = PyntCloud.from_file(str(data_path / "obj_issue_vn.obj"))

    assert len(cloud.xyz) == 3
    assert len(cloud.mesh) == 1


def test_ply_with_bool(data_path):
    """Expectation: a PLY file that contains bool types can be read into a PyntCloud object."""
    TEST_PLY = str(data_path / "diamond_with_bool.ply")

    with pytest.raises(KeyError, match="bool"):
        cloud = PyntCloud.from_file(TEST_PLY)

    cloud = PyntCloud.from_file(filename=TEST_PLY, allow_bool=True)
    assert "is_green" in cloud.points.columns, "Failed to find expected Boolean column: 'is_green'"
    assert cloud.points.is_green.dtype == bool, "Boolean column no loaded as bool dtype"


def test_simple_las_issue_333(data_path):
    """ Regression test https://github.com/daavoo/pyntcloud/issues/333
    """
    las_file_name = (str(data_path / "simple.las"))
    cloud = PyntCloud.from_file(las_file_name)
    points = cloud.points

    x_point_pyntcloud = points["x"][0]
    y_point_pyntcloud = points["y"][0]
    z_point_pyntcloud = points["z"][0]

    import laspy
    with laspy.open(las_file_name) as las_file:
        las = las_file.read()
        header = las.header

        x_point_laspy = (las.X[0] * header.x_scale) + header.x_offset
        y_point_laspy = (las.Y[0] * header.y_scale) + header.y_offset
        z_point_laspy = (las.Z[0] * header.z_scale) + header.z_offset

    assert x_point_pyntcloud == x_point_laspy
    assert y_point_pyntcloud == y_point_laspy
    assert z_point_pyntcloud == z_point_laspy


def test_has_offsets_las_issue_333(data_path):
    """ Regression test https://github.com/daavoo/pyntcloud/issues/333
    """
    las_file_name = (str(data_path / "has_offsets.las"))
    cloud = PyntCloud.from_file(las_file_name)
    points = cloud.points

    x_point_pyntcloud = points["x"][0]
    y_point_pyntcloud = points["y"][0]
    z_point_pyntcloud = points["z"][0]

    import laspy
    with laspy.open(las_file_name) as las_file:
        las = las_file.read()
        header = las.header

        x_point_laspy = (las.X[0] * header.x_scale) + header.x_offset
        y_point_laspy = (las.Y[0] * header.y_scale) + header.y_offset
        z_point_laspy = (las.Z[0] * header.z_scale) + header.z_offset

    assert x_point_pyntcloud == x_point_laspy
    assert y_point_pyntcloud == y_point_laspy
    assert z_point_pyntcloud == z_point_laspy
