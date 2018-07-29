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


@pytest.mark.parametrize("extension,color,mesh", [
    (".ply", True, True),
    ("_ascii.ply", True, True),
    (".npz", True, True),
    (".obj", False, False),
    (".off", False, False),
    ("_color.off", True, False),
    (".bin", False, False)
])
def test_from_file(data_path, extension, color, mesh):
    file = PyntCloud.from_file(str(data_path / "diamond{}".format(extension)))
    assert_points_xyz(file)
    if color:
        assert_points_color(file)
    if mesh:
        assert_mesh(file)
