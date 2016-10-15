import os

from pyntcloud.io.npz import read_npz, write_npz
from pyntcloud.io.obj import read_obj, write_obj
from pyntcloud.io.pcd import read_pcd, write_pcd
from pyntcloud.io.ply import read_ply, write_ply

# just in case test are being runned from other directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
data_path = '../data/python'


def assert_points_xyz(data):
    assert data['points']['x'][23] == -1.5
    assert data['points']['y'][23] == -5.5
    assert data['points']['z'][23] == 1.5

    assert str(data['points']["x"].dtype) == 'float32'
    assert str(data['points']["y"].dtype) == 'float32'
    assert str(data['points']["z"].dtype) == 'float32'
    
def assert_points_color(data):
    assert data['points']['red'][23] == 0
    assert data['points']['green'][23] == 170
    assert data['points']['blue'][23] == 255

    assert str(data['points']['red'].dtype) == 'uint8'
    assert str(data['points']['green'].dtype) == 'uint8'
    assert str(data['points']['blue'].dtype) == 'uint8'

def assert_ply_mesh(data):
    assert data["mesh"]["v1"][23] == 227
    assert data["mesh"]["v2"][23] == 225
    assert data["mesh"]["v3"][23] == 223

    assert str(data['mesh']['v1'].dtype) == 'int32'
    assert str(data['mesh']['v2'].dtype) == 'int32'
    assert str(data['mesh']['v3'].dtype) == 'int32'


def test_read_ply_bin():
    ply_bin = read_ply(data_path + '_bin.ply')

    assert_points_xyz(ply_bin)
    assert_points_color(ply_bin)
    assert_ply_mesh(ply_bin)    


def test_read_ply_ascii():
    ply_ascii = read_ply(data_path + '.ply')

    assert_points_xyz(ply_ascii)
    assert_points_color(ply_ascii)
    assert_ply_mesh(ply_ascii)   
    
    
def test_write_ply():
    data = read_ply(data_path + '_bin.ply')    
    
    write_ply(data_path + 'writed_ascii.ply', points=data["points"], mesh=data["mesh"],
              comments=data["comments"], obj_info=data["obj_info"], as_text=True)  
    write_ply(data_path + 'writed_bin.ply', points=data["points"], mesh=data["mesh"],
              comments=data["comments"], obj_info=data["obj_info"], as_text=False) 
              
    writed_ply_ascii = read_ply(data_path + 'writed_ascii.ply')
    writed_ply_bin = read_ply(data_path + 'writed_bin.ply')
    
    assert all(data["points"] == writed_ply_ascii["points"])
    assert all(data["points"] == writed_ply_bin["points"])
    assert all(data["mesh"] == writed_ply_ascii["mesh"])
    assert all(data["mesh"] == writed_ply_bin["mesh"])

    os.remove(data_path + 'writed_ascii.ply')
    os.remove(data_path + 'writed_bin.ply')


def test_read_npz():
    npz = read_npz(data_path + '.npz')

    assert_points_xyz(npz)
    assert_points_color(npz)
    assert_ply_mesh(npz)    
    
    
def test_write_npz():
    data = read_ply(data_path + '_bin.ply')    

    write_npz(data_path + 'writed_npz.npz', points=data["points"], mesh=data["mesh"],
              comments=data["comments"], obj_info=data["obj_info"])  

    writed_npz = read_npz(data_path + 'writed_npz.npz')

    assert all(data["points"] == writed_npz["points"])
    assert all(data["mesh"] == writed_npz["mesh"])

    os.remove(data_path + 'writed_npz.npz')


def test_read_obj():
    obj = read_obj(data_path + '.obj')
    
    assert_points_xyz(obj)


def test_write_obj():
    data = read_ply(data_path + '_bin.ply')    
    
    write_obj(data_path + 'writed.obj', points=data["points"], mesh=data["mesh"],
              comments=data["comments"], obj_info=data["obj_info"])  

    writed_obj = read_obj(data_path + 'writed.obj')
    
    assert all(data["points"][["x", "y", "z"]] == writed_obj["points"])
    
    os.remove(data_path + 'writed.obj')


def test_read_pcd():
    pcd = read_pcd(data_path + '.pcd')
    
    assert_points_xyz(pcd)
    assert_points_color(pcd)

