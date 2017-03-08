import os
import pytest

from numpy import pi as PI

from pyntcloud import PyntCloud

cloud = PyntCloud.from_file('data/sf/xyz_rgb_nxnynz.npz')


def test_inclination_deg():
    
    cloud.add_scalar_field('inclination_deg')

    assert min(cloud.points["inclination_deg"]) >= 0
    assert max(cloud.points["inclination_deg"]) <= 180

    cloud.points.drop("inclination_deg", 1, inplace=True)


def test_inclination_rad():
    
    cloud.add_scalar_field('inclination_rad')

    assert min(cloud.points["inclination_rad"]) >= 0
    assert max(cloud.points["inclination_rad"]) <= PI

    cloud.points.drop("inclination_rad", 1, inplace=True)


def test_orientation_deg():
    
    cloud.add_scalar_field('orientation_deg')

    assert min(cloud.points["orientation_deg"]) >= 0
    assert max(cloud.points["orientation_deg"]) <= 360

    cloud.points.drop("orientation_deg", 1, inplace=True)


def test_orientation_rad():
    
    cloud.add_scalar_field('orientation_rad')

    assert min(cloud.points["orientation_rad"]) >= 0
    assert max(cloud.points["orientation_rad"]) <= 2 * PI

    cloud.points.drop("orientation_rad", 1, inplace=True)


def test_rgb_sf():
    
    # RGB Intensity
    cloud.add_scalar_field('rgb_intensity')

    assert min(cloud.points["Ri"]) >= 0
    assert min(cloud.points["Gi"]) >= 0
    assert min(cloud.points["Bi"]) >= 0
    assert max(cloud.points["Ri"]) <= 1
    assert max(cloud.points["Gi"]) <= 1
    assert max(cloud.points["Bi"]) <= 1

    cloud.points.drop(["Ri", "Gi", "Bi"], 1, inplace=True)
    
    # Relative Luminance    
    cloud.add_scalar_field('relative_luminance')

    assert min(cloud.points["relative_luminance"]) >= 0
    assert max(cloud.points["relative_luminance"]) < 255.01  

    cloud.points.drop("relative_luminance", 1, inplace=True)
    
    # HSV
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
        # missing structure
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
        

