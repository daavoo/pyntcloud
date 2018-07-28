import os
import numpy as np
from pyntcloud import PyntCloud
import pytest

path = os.path.abspath(os.path.dirname(__file__))
data_path = path + '/data/diamond'


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


def test_read_ply_bin():
    ply_bin = PyntCloud.from_file(data_path + '.ply')

    assert_points_xyz(ply_bin)
    assert_points_color(ply_bin)
    assert_mesh(ply_bin)


def test_read_ply_ascii():
    ply_ascii = PyntCloud.from_file(data_path + '_ascii.ply')

    assert_points_xyz(ply_ascii)
    assert_points_color(ply_ascii)
    assert_mesh(ply_ascii)


def test_write_ply():
    data = PyntCloud.from_file(data_path + '.ply')

    data.to_file(data_path + 'writed_ascii.ply', also_save=["mesh"],
                 as_text=True)
    data.to_file(data_path + 'writed_bin.ply', also_save=["mesh"],
                 as_text=False)

    writed_ply_ascii = PyntCloud.from_file(data_path + 'writed_ascii.ply')
    writed_ply_bin = PyntCloud.from_file(data_path + 'writed_bin.ply')

    assert all(data.points == writed_ply_ascii.points)
    assert all(data.points == writed_ply_bin.points)
    assert all(data.mesh == writed_ply_ascii.mesh)
    assert all(data.mesh == writed_ply_bin.mesh)

    os.remove(data_path + 'writed_ascii.ply')
    os.remove(data_path + 'writed_bin.ply')


def test_read_npz():
    npz = PyntCloud.from_file(data_path + '.npz')

    assert_points_xyz(npz)
    assert_points_color(npz)
    assert_mesh(npz)


def test_write_npz():
    data = PyntCloud.from_file(data_path + '.ply')

    data.to_file(data_path + 'written_npz.npz', also_save=["mesh"])

    written_npz = PyntCloud.from_file(data_path + 'written_npz.npz')

    assert all(data.points == written_npz.points)
    assert all(data.mesh == written_npz.mesh)

    os.remove(data_path + 'written_npz.npz')


def test_read_obj():
    obj = PyntCloud.from_file(data_path + '.obj')

    assert_points_xyz(obj)


def test_write_obj():
    data = PyntCloud.from_file(data_path + '.ply')

    data.to_file(data_path + 'written.obj', also_save=["mesh"])

    written_obj = PyntCloud.from_file(data_path + 'written.obj')

    assert all(data.points[["x", "y", "z"]] == written_obj.points)
    assert all(data.mesh[["v1", "v2", "v3"]] == written_obj.mesh)

    os.remove(data_path + 'written.obj')


def test_read_ascii():
    data = PyntCloud.from_file(data_path + '.xyz', sep=" ", header=None,
                               index_col=False,
                               names=["x", "y", "z", "nx", "ny", "nz"],
                               dtype="f")

    assert_points_xyz(data)


def test_write_ascii():
    data = PyntCloud.from_file(
        data_path + '.xyz',
        sep=" ",
        header=None,
        index_col=False,
        names=["x", "y", "z", "nx", "ny", "nz"],
        dtype="f")

    data.to_file(data_path + 'written.txt', sep=" ", header=None)

    written_data = PyntCloud.from_file(
        data_path + 'written.txt',
        sep=" ",
        header=None,
        index_col=False,
        names=["x", "y", "z", "nx", "ny", "nz"],
        dtype="f")

    assert all(data.points == written_data.points)

    os.remove(data_path + 'written.txt')


def test_read_off():
    off = PyntCloud.from_file(data_path + '.off')

    assert_points_xyz(off)


def test_read_color_off():
    color_off = PyntCloud.from_file(data_path + '_color.off')

    assert_points_xyz(color_off)
    assert_points_color(color_off)


def test_read_bin():
    arr = PyntCloud.from_file(data_path + '.bin')

    assert_points_xyz(arr)


def test_write_bin():

    data = PyntCloud.from_file(data_path + '.bin')

    data.to_file(data_path + 'written.bin')

    # write_bin only accepts kwargs: "sep" and "format" for numpy.ndarray.tofile()
    with pytest.raises(ValueError):
        data.to_file(data_path + '_fail.bin', also_save=['mesh'])
    with pytest.raises(ValueError):
        data.to_file(data_path + '_fail.bin', some_other_kwarg='some_value')
    
    written_data = PyntCloud.from_file(data_path + 'written.bin')

    assert_points_xyz(written_data)
    assert np.array_equal(data.points, written_data.points)
    assert np.array_equal(data.xyz, written_data.xyz)

    os.remove(data_path + 'written.bin')

    
