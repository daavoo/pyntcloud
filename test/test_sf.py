import os
import pytest

from numpy import pi as PI

from pyntcloud import PyntCloud

# just in case test are being runned from other directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
cloud = PyntCloud.from_file('../docs/data/test/test_bin.ply')


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


def test_rgb_intensity():
    
    cloud.add_scalar_field('rgb_intensity')

    assert min(cloud.points["Ri"]) >= 0
    assert min(cloud.points["Gi"]) >= 0
    assert min(cloud.points["Bi"]) >= 0
    assert max(cloud.points["Ri"]) <= 1
    assert max(cloud.points["Gi"]) <= 1
    assert max(cloud.points["Bi"]) <= 1

    cloud.points.drop(["Ri", "Gi", "Bi"], 1, inplace=True)


def test_relative_luminance():
    
    cloud.add_scalar_field('relative_luminance')

    assert min(cloud.points["relative_luminance"]) >= 0
    assert max(cloud.points["relative_luminance"]) < 255.01  

    cloud.points.drop("relative_luminance", 1, inplace=True)


def test_hsv():

    cloud.add_scalar_field('hsv')

    assert min(cloud.points["H"]) >= 0
    assert max(cloud.points["H"]) <= 360
    assert min(cloud.points["S"]) >= 0
    assert max(cloud.points["S"]) <= 1
    assert min(cloud.points["V"]) >= 0
    assert max(cloud.points["V"]) <= 100

    cloud.points.drop(["H", "S", "V"], 1, inplace=True)


def test_octree():
    cloud.add_structure("octree")

    with pytest.raises(ValueError):
        cloud.add_scalar_field("octree_level", octree="O(2)", level=3)

    cloud.add_scalar_field("octree_level", octree="O(2)", level=2)

    assert min(cloud.points["octree_level(2,O(2))"]) == 0
    assert max(cloud.points["octree_level(2,O(2))"]) == 77

