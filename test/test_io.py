import os

from pyntcloud.io.npz import read_npz, write_npz
from pyntcloud.io.obj import read_obj, write_obj
from pyntcloud.io.ply import read_ply, write_ply

# just in case test are being runned from other directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
data_path = '../data/python'


def assert_vertex_xyz(data):
    assert data['vertex']['x'][23] == -1.5
    assert data['vertex']['y'][23] == -5.5
    assert data['vertex']['z'][23] == 1.5

    assert str(data['vertex']["x"].dtype) == 'float32'
    assert str(data['vertex']["y"].dtype) == 'float32'
    assert str(data['vertex']["z"].dtype) == 'float32'
    
def assert_vertex_color(data):
    assert data['vertex']['red'][23] == 0
    assert data['vertex']['green'][23] == 170
    assert data['vertex']['blue'][23] == 255

    assert str(data['vertex']['red'].dtype) == 'uint8'
    assert str(data['vertex']['green'].dtype) == 'uint8'
    assert str(data['vertex']['blue'].dtype) == 'uint8'

def assert_ply_face(data):
    assert data["face"]["v1"][23] == 227
    assert data["face"]["v2"][23] == 225
    assert data["face"]["v3"][23] == 223

    assert str(data['face']['v1'].dtype) == 'int32'
    assert str(data['face']['v2'].dtype) == 'int32'
    assert str(data['face']['v3'].dtype) == 'int32'


def test_read_ply_bin():
    ply_bin = read_ply(data_path + '_bin.ply')

    assert_vertex_xyz(ply_bin)
    assert_vertex_color(ply_bin)
    assert_ply_face(ply_bin)    


def test_read_ply_ascii():
    ply_ascii = read_ply(data_path + '.ply')

    assert_vertex_xyz(ply_ascii)
    assert_vertex_color(ply_ascii)
    assert_ply_face(ply_ascii)   
    
    
def test_write_ply():
    data = read_ply(data_path + '_bin.ply')    
    
    write_ply(data_path + 'writed_ascii.ply', vertex=data["vertex"], face=data["face"],
              comments=data["comments"], obj_info=data["obj_info"], as_text=True)  
    write_ply(data_path + 'writed_bin.ply', vertex=data["vertex"], face=data["face"],
              comments=data["comments"], obj_info=data["obj_info"], as_text=False) 
              
    writed_ply_ascii = read_ply(data_path + 'writed_ascii.ply')
    writed_ply_bin = read_ply(data_path + 'writed_bin.ply')
    
    assert all(data["vertex"] == writed_ply_ascii["vertex"])
    assert all(data["vertex"] == writed_ply_bin["vertex"])
    assert all(data["face"] == writed_ply_ascii["face"])
    assert all(data["face"] == writed_ply_bin["face"])

    os.remove(data_path + 'writed_ascii.ply')
    os.remove(data_path + 'writed_bin.ply')


def test_read_npz():
    npz = read_npz(data_path + '.npz')

    assert_vertex_xyz(npz)
    assert_vertex_color(npz)
    assert_ply_face(npz)    
    
    
def test_write_npz():
    data = read_ply(data_path + '_bin.ply')    

    write_npz(data_path + 'writed_npz.npz', vertex=data["vertex"], face=data["face"],
              comments=data["comments"], obj_info=data["obj_info"])  

    writed_npz = read_npz(data_path + 'writed_npz.npz')

    assert all(data["vertex"] == writed_npz["vertex"])
    assert all(data["face"] == writed_npz["face"])

    os.remove(data_path + 'writed_npz.npz')


def test_read_obj():
    obj = read_obj(data_path + '.obj')
    
    assert_vertex_xyz(obj)


def test_write_obj():
    data = read_ply(data_path + '_bin.ply')    
    
    write_obj(data_path + 'writed.obj', vertex=data["vertex"], face=data["face"],
              comments=data["comments"], obj_info=data["obj_info"])  

    writed_obj = read_obj(data_path + 'writed.obj')
    
    assert all(data["vertex"][["x", "y", "z"]] == writed_obj["vertex"])
    
    os.remove(data_path + 'writed.obj')


def test_read_pcd():
    pcd = read_obj(data_path + '.pcd')
    
    assert_vertex_xyz(pcd)
    assert_vertex_color(pcd)

