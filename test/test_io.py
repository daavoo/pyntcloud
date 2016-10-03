import os

from pyntcloud.io.npz import read_npz, write_npz
from pyntcloud.io.obj import read_obj #, write_obj
from pyntcloud.io.ply import read_ply, write_ply

# just in case test are being runned from other directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
data_path = '../data/python'

def assert_data(data):
    assert data['vertex']['x'][0] == -6.5
    assert data['face']['v1'][0] == data['face']['v1'][0]
    assert data['comments'][0].split()[2] == data['comments'][0].split()[2]
    assert data['obj_info'][0].split()[1] == data['obj_info'][0].split()[1]
    assert str(data['vertex']['x'].dtype) == 'float32'
    assert str(data['face']['v1'].dtype) == 'int32'
    

def assert_data1_data2(data1, data2):
    assert data1['vertex']['x'][0] == data2['vertex']['x'][0]
    assert data1['face']['v1'][0] == data2['face']['v1'][0]
    assert data1['comments'][0].split()[2] == data2['comments'][0].split()[2]
    assert data1['obj_info'][0].split()[1] == data2['obj_info'][0].split()[1]
    assert str(data1['vertex']['x'].dtype) == str(data2['vertex']['x'].dtype)
    assert str(data1['face']['v1'].dtype) == str(data2['face']['v1'].dtype)


def assert_color(data):
    assert data['vertex']['green'][0] == 170
    assert str(data['vertex']['red'].dtype) == 'uint8'


def assert_color_data1_data2(data1, data2):
    assert data1['vertex']['green'][0] == data2['vertex']['green'][0]
    assert str(data1['vertex']['red'].dtype) == str(data2['vertex']['red'].dtype)


def test_read_ply_bin():
    ply_bin = read_ply(data_path + '_bin.ply')
    assert_data(ply_bin)
    assert_color(ply_bin)


def test_read_ply_ascii():
    ply_ascii = read_ply(data_path + '.ply')
    assert_data(ply_ascii)
    assert_color(ply_ascii)
    
    
def test_write_ply():
    data = read_ply(data_path + '_bin.ply')    
    
    write_ply(data_path + 'writed_ascii.ply', vertex=data["vertex"], face=data["face"],
              comments=data["comments"], obj_info=data["obj_info"], as_text=True)  
    write_ply(data_path + 'writed_bin.ply', vertex=data["vertex"], face=data["face"],
              comments=data["comments"], obj_info=data["obj_info"], as_text=False) 
              
    writed_ply_ascii = read_ply(data_path + 'writed_ascii.ply')
    writed_ply_bin = read_ply(data_path + 'writed_bin.ply')
    
    assert_data1_data2(data, writed_ply_ascii)
    assert_color_data1_data2(data, writed_ply_ascii)

    assert_data1_data2(writed_ply_ascii, writed_ply_bin)
    assert_color_data1_data2(data, writed_ply_bin)
    
    os.remove(data_path + 'writed_ascii.ply')
    os.remove(data_path + 'writed_bin.ply')


def test_read_npz():
    npz = read_npz(data_path + '.npz')
    assert_data(npz)
    assert_color(npz)
    
    
def test_write_npz():
    data = read_ply(data_path + '_bin.ply')    
    
    write_npz(data_path + 'writed_npz.npz', vertex=data["vertex"], face=data["face"],
              comments=data["comments"], obj_info=data["obj_info"])  

    writed_npz = read_npz(data_path + 'writed_npz.npz')
    
    assert_data1_data2(data, writed_npz)
    assert_color_data1_data2(data, writed_npz)
    
    os.remove(data_path + 'writed_npz.npz')


def test_read_obj():
    obj = read_obj(data_path + '.obj')
    assert_data(obj)


'''
def test_write_obj():
    data = read_ply(data_path + '_bin.ply')    
    
    write_obj(data_path + 'writed_npz.npz', vertex=data["vertex"], face=data["face"],
              comments=data["comments"], obj_info=data["obj_info"])  

    writed_obj = read_npz(data_path + 'writed_obj.obj')
    
    assert_data1_data2(data, writed_obj)
    
    os.remove(data_path + 'writed_obj.obj')
'''