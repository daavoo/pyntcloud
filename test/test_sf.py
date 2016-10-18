import os
from numpy import pi as PI

from pyntcloud import PyntCloud

# just in case test are being runned from other directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sphere = PyntCloud.from_file('../data/sphere.ply')


def test_inclination_deg():
    
    sphere.add_scalar_field('inclination_deg')

    assert min(sphere.points["inclination_deg"]) >= 0
    assert max(sphere.points["inclination_deg"]) <= 180
    assert sphere.points[sphere.points.x == sphere.points.x.max()]["inclination_deg"].values[0] > 89
    assert sphere.points[sphere.points.x == sphere.points.x.max()]["inclination_deg"].values[0] < 91
    assert sphere.points[sphere.points.y == sphere.points.y.max()]["inclination_deg"].values[0] > 89
    assert sphere.points[sphere.points.y == sphere.points.y.max()]["inclination_deg"].values[0] < 91
    assert sphere.points[sphere.points.z == sphere.points.z.max()]["inclination_deg"].values[0] > -1
    assert sphere.points[sphere.points.z == sphere.points.z.max()]["inclination_deg"].values[0] < 1

    sphere.points.drop("inclination_deg", 1, inplace=True)


def test_inclination_rad():
    
    sphere.add_scalar_field('inclination_rad')

    assert min(sphere.points["inclination_rad"]) >= 0
    assert max(sphere.points["inclination_rad"]) <= PI
    assert sphere.points[sphere.points.x == sphere.points.x.max()]["inclination_rad"].values[0] > (PI/2) - 1
    assert sphere.points[sphere.points.x == sphere.points.x.max()]["inclination_rad"].values[0] < (PI/2) + 1
    assert sphere.points[sphere.points.y == sphere.points.y.max()]["inclination_rad"].values[0] > (PI/2) - 1
    assert sphere.points[sphere.points.y == sphere.points.y.max()]["inclination_rad"].values[0] < (PI/2) + 1
    assert sphere.points[sphere.points.z == sphere.points.z.max()]["inclination_rad"].values[0] > -1
    assert sphere.points[sphere.points.z == sphere.points.z.max()]["inclination_rad"].values[0] < 1

    sphere.points.drop("inclination_rad", 1, inplace=True)


def test_orientation_deg():
    
    sphere.add_scalar_field('orientation_deg')

    assert min(sphere.points["orientation_deg"]) >= 0
    assert max(sphere.points["orientation_deg"]) <= 360
    assert sphere.points[sphere.points.x == sphere.points.x.max()]["orientation_deg"].values[0] > 89
    assert sphere.points[sphere.points.x == sphere.points.x.max()]["orientation_deg"].values[0] < 91
    assert sphere.points[sphere.points.x == sphere.points.x.min()]["orientation_deg"].values[0] > 269
    assert sphere.points[sphere.points.x == sphere.points.x.min()]["orientation_deg"].values[0] < 271
    assert sphere.points[sphere.points.y == sphere.points.y.min()]["orientation_deg"].values[0] > 179
    assert sphere.points[sphere.points.y == sphere.points.y.min()]["orientation_deg"].values[0] < 181

    sphere.points.drop("orientation_deg", 1, inplace=True)


def test_orientation_rad():
    
    sphere.add_scalar_field('orientation_rad')

    assert min(sphere.points["orientation_rad"]) >= 0
    assert max(sphere.points["orientation_rad"]) <= 2 * PI
    assert sphere.points[sphere.points.x == sphere.points.x.max()]["orientation_rad"].values[0] > (PI/2) - 1
    assert sphere.points[sphere.points.x == sphere.points.x.max()]["orientation_rad"].values[0] < (PI/2) + 1
    assert sphere.points[sphere.points.x == sphere.points.x.min()]["orientation_rad"].values[0] > (3/2 * PI) - 1
    assert sphere.points[sphere.points.x == sphere.points.x.min()]["orientation_rad"].values[0] < (3/2 * PI) + 1
    assert sphere.points[sphere.points.y == sphere.points.y.min()]["orientation_rad"].values[0] > PI - 1
    assert sphere.points[sphere.points.y == sphere.points.y.min()]["orientation_rad"].values[0] < PI + 1

    sphere.points.drop("orientation_rad", 1, inplace=True)


def test_rgb_intensity():
    
    sphere.add_scalar_field('rgb_intensity')

    assert min(sphere.points["Ri"]) >= 0
    assert min(sphere.points["Gi"]) >= 0
    assert min(sphere.points["Bi"]) >= 0
    assert max(sphere.points["Ri"]) <= 1
    assert max(sphere.points["Gi"]) <= 1
    assert max(sphere.points["Bi"]) <= 1

    sphere.points.drop(["Ri", "Gi", "Bi"], 1, inplace=True)


def test_relative_luminance():
    
    sphere.add_scalar_field('relative_luminance')

    assert min(sphere.points["relative_luminance"]) >= 0
    assert max(sphere.points["relative_luminance"]) < 255.01  # floating point error

    sphere.points.drop("relative_luminance", 1, inplace=True)