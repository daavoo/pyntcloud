import os
import pytest
import numpy as np
from pyntcloud import PyntCloud

PI = np.pi + 0.01

path = os.path.abspath(os.path.dirname(__file__))
cloud = PyntCloud.from_file(path + "/data/mnist.npz")

def test_eigenvalues():
    
    k_neighbors = cloud.get_neighbors(k=5)
    ev = cloud.add_scalar_field("eigen_values", k_neighbors=k_neighbors)
    
    with pytest.raises(TypeError):
        # missing arg
        cloud.add_scalar_field("sphericity")
        
    cloud.add_scalar_field("sphericity", ev=ev) 
    cloud.points.drop("sphericity(5)", 1, inplace=True)
    cloud.add_scalar_field("anisotropy", ev=ev) 
    cloud.points.drop("anisotropy(5)", 1, inplace=True)
    cloud.add_scalar_field("linearity", ev=ev)
    cloud.points.drop("linearity(5)", 1, inplace=True)    
    cloud.add_scalar_field("omnivariance", ev=ev)
    cloud.points.drop("omnivariance(5)", 1, inplace=True) 
    cloud.add_scalar_field("eigenentropy", ev=ev)
    cloud.points.drop("eigenentropy(5)", 1, inplace=True) 
    cloud.add_scalar_field("planarity", ev=ev)
    cloud.points.drop("planarity(5)", 1, inplace=True)
    cloud.add_scalar_field("eigen_sum", ev=ev)
    cloud.points.drop("eigen_sum(5)", 1, inplace=True)
    cloud.add_scalar_field("curvature", ev=ev)
    cloud.points.drop("curvature(5)", 1, inplace=True)
    
def test_k_neighbors():
    
    k_neighbors = cloud.get_neighbors(k=5)
    
    with pytest.raises(TypeError):
        # missing arg
        cloud.add_scalar_field("eigen_values")
        
    ev = cloud.add_scalar_field("eigen_values", k_neighbors=k_neighbors)
    assert ev[0] == "e1(5)"
    
    ev = ev = cloud.add_scalar_field("eigen_decomposition", k_neighbors=k_neighbors)
    assert ev[3] == "ev1(5)"
    idx =  np.random.randint(0, 100)
    for i in [3,4,5]:
        assert np.linalg.norm(cloud.points[ev[i]][idx]) > 0.99
        assert np.linalg.norm(cloud.points[ev[i]][idx]) < 1.01

def test_normals_sf():
    
    cloud.add_scalar_field('inclination_deg')
    assert min(cloud.points["inclination_deg"]) >= 0
    assert max(cloud.points["inclination_deg"]) <= 180
    cloud.points.drop("inclination_deg", 1, inplace=True)
    
    cloud.add_scalar_field('inclination_rad')
    assert min(cloud.points["inclination_rad"]) >= 0
    assert max(cloud.points["inclination_rad"]) <= PI
    cloud.points.drop("inclination_rad", 1, inplace=True)
    
    cloud.add_scalar_field('orientation_deg')
    assert min(cloud.points["orientation_deg"]) >= 0
    assert max(cloud.points["orientation_deg"]) <= 360
    cloud.points.drop("orientation_deg", 1, inplace=True)
    
    cloud.add_scalar_field('orientation_rad')
    assert min(cloud.points["orientation_rad"]) >= 0
    assert max(cloud.points["orientation_rad"]) <= 2 * PI
    cloud.points.drop("orientation_rad", 1, inplace=True)


def test_rgb_sf():
    
    cloud.add_scalar_field('rgb_intensity')
    assert min(cloud.points["Ri"]) >= 0
    assert min(cloud.points["Gi"]) >= 0
    assert min(cloud.points["Bi"]) >= 0
    assert max(cloud.points["Ri"]) <= 1
    assert max(cloud.points["Gi"]) <= 1
    assert max(cloud.points["Bi"]) <= 1
    cloud.points.drop(["Ri", "Gi", "Bi"], 1, inplace=True)
    
    cloud.add_scalar_field('relative_luminance')
    assert min(cloud.points["relative_luminance"]) >= 0
    assert max(cloud.points["relative_luminance"]) < 255.01  
    cloud.points.drop("relative_luminance", 1, inplace=True)
    
    cloud.add_scalar_field('hsv')
    assert min(cloud.points["H"]) >= 0
    assert max(cloud.points["H"]) <= 360
    assert min(cloud.points["S"]) >= 0
    assert max(cloud.points["S"]) <= 1
    assert min(cloud.points["V"]) >= 0
    assert max(cloud.points["V"]) <= 100
    cloud.points.drop(["H", "S", "V"], 1, inplace=True)
    

def test_voxelgrid_sf():

    with pytest.raises(TypeError):
        # missing arg
        cloud.add_scalar_field("voxel_x")

    vg_id = cloud.add_structure("voxelgrid", x_y_z=[2,2,2])

    with pytest.raises(KeyError):
        # wrong id
        cloud.add_scalar_field("voxel_x", voxelgrid="V([1,1,1],True)")
    
    for sf in {"voxel_x", "voxel_y", "voxel_z"}:
        cloud.add_scalar_field(sf, voxelgrid=vg_id)
        sf_id = "{}({})".format(sf, vg_id)
        assert min(cloud.points[sf_id]) >= 0
        assert max(cloud.points[sf_id]) <= 1
        cloud.points.drop(sf_id, 1, inplace=True)

    cloud.add_scalar_field("voxel_n", voxelgrid=vg_id)
    sf_id = "voxel_n({})".format(vg_id)
    assert min(cloud.points[sf_id]) >= 0
    assert max(cloud.points[sf_id]) <= 7
    cloud.points.drop(sf_id, 1, inplace=True)
        

