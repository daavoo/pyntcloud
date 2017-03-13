import os

from pyntcloud import PyntCloud

os.chdir(os.path.abspath(os.path.dirname(__file__)))
data_path = '\\data\\io\\test'

def assert_points_xyz(data):
    assert data.points['x'][7] == 1.0
    assert data.points['y'][7] == 1.0
    assert data.points['z'][7] == 1.0

    assert str(data.points["x"].dtype) == 'float32'
    assert str(data.points["y"].dtype) == 'float32'
    assert str(data.points["z"].dtype) == 'float32'
    
def assert_points_color(data):
    assert data.points['red'][7] == 255
    assert data.points['green'][7] == 0
    assert data.points['blue'][7] == 0

    assert str(data.points['red'].dtype) == 'uint8'
    assert str(data.points['green'].dtype) == 'uint8'
    assert str(data.points['blue'].dtype) == 'uint8'

def assert_mesh(data):
    assert data.mesh["v1"][0] == 3
    assert data.mesh["v2"][0] == 1
    assert data.mesh["v3"][0] == 4

    assert str(data.mesh['v1'].dtype) == 'int32'
    assert str(data.mesh['v2'].dtype) == 'int32'
    assert str(data.mesh['v3'].dtype) == 'int32'


def test_read_ply_bin():
    ply_bin = PyntCloud.from_file(data_path + '_bin.ply')

    assert_points_xyz(ply_bin)
    assert_points_color(ply_bin)
    assert_mesh(ply_bin)    


def test_read_ply_ascii():
    ply_ascii = PyntCloud.from_file(data_path + '.ply')

    assert_points_xyz(ply_ascii)
    assert_points_color(ply_ascii)
    assert_mesh(ply_ascii)   
    
    
def test_write_ply():
    data = PyntCloud.from_file(data_path + '_bin.ply')    
    
    data.to_file(data_path + 'writed_ascii.ply', internal=["points", "mesh"], as_text=True)  
    data.to_file(data_path + 'writed_bin.ply', internal=["points", "mesh"], as_text=False) 
              
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
    data = PyntCloud.from_file(data_path + '_bin.ply')    

    data.to_file(data_path + 'writed_npz.npz', internal=["points", "mesh"])  

    writed_npz = PyntCloud.from_file(data_path + 'writed_npz.npz')

    assert all(data.points == writed_npz.points)
    assert all(data.mesh == writed_npz.mesh)

    os.remove(data_path + 'writed_npz.npz')


def test_read_obj():
    obj = PyntCloud.from_file(data_path + '.obj')
    
    assert_points_xyz(obj)


def test_write_obj():
    data = PyntCloud.from_file(data_path + '_bin.ply')    
    
    data.to_file(data_path + 'writed.obj', internal=["points", "mesh"])  

    writed_obj = PyntCloud.from_file(data_path + 'writed.obj')
    
    assert all(data.points[["x", "y", "z"]] == writed_obj.points)
    
    os.remove(data_path + 'writed.obj')

def test_read_mat():
    mat = PyntCloud.from_file(data_path + '.mat')
    
    assert_points_xyz(mat)
    assert_points_color(mat)
    assert_mesh(mat)


