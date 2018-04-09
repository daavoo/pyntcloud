import pytest

import numpy as np

from pyntcloud.scalar_fields.xyz import (
    PlaneFit,
    SphereFit,
    SphericalCoordinates,
    CylindricalCoordinates
)


@pytest.mark.usefixtures("plane_pyntcloud")
def test_PlaneFit_max_dist(plane_pyntcloud):
    scalar_field = PlaneFit(
        pyntcloud=plane_pyntcloud)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    assert sum(scalar_field.to_be_added["is_plane"]) == 4

    scalar_field = PlaneFit(
        pyntcloud=plane_pyntcloud,
        max_dist=0.4)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    assert sum(scalar_field.to_be_added["is_plane"]) == 5


@pytest.mark.usefixtures("sphere_pyntcloud")
def test_SphereFit_max_dist(sphere_pyntcloud):
    scalar_field = SphereFit(
        pyntcloud=sphere_pyntcloud)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    assert sum(scalar_field.to_be_added["is_sphere"]) == 4

    scalar_field = SphereFit(
        pyntcloud=sphere_pyntcloud,
        max_dist=0.25)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    assert sum(scalar_field.to_be_added["is_sphere"]) == 5


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_SphericalCoordinates_bounds(pyntcloud_with_rgb_and_normals):
    scalar_field = SphericalCoordinates(
        pyntcloud=pyntcloud_with_rgb_and_normals)
    scalar_field.extract_info()

    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()

    assert all(scalar_field.to_be_added["polar"] >= 0)
    assert all(scalar_field.to_be_added["polar"] <= 180)

    assert all(scalar_field.to_be_added["azimuthal"] >= -180)
    assert all(scalar_field.to_be_added["azimuthal"] <= 180)

    scalar_field = SphericalCoordinates(
        pyntcloud=pyntcloud_with_rgb_and_normals,
        degrees=False)
    scalar_field.extract_info()

    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()

    assert all(scalar_field.to_be_added["polar"] >= 0)
    assert all(scalar_field.to_be_added["polar"] <= np.pi)

    assert all(scalar_field.to_be_added["azimuthal"] >= -np.pi)
    assert all(scalar_field.to_be_added["azimuthal"] <= np.pi)


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_CylindricalCoordinates_bounds(pyntcloud_with_rgb_and_normals):
    scalar_field = CylindricalCoordinates(
        pyntcloud=pyntcloud_with_rgb_and_normals)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()

    assert all(scalar_field.to_be_added["angular_cylindrical"] >= -90)
    assert all(scalar_field.to_be_added["angular_cylindrical"] <= 270)

    scalar_field = CylindricalCoordinates(
        pyntcloud=pyntcloud_with_rgb_and_normals,
        degrees=False)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()

    assert all(scalar_field.to_be_added["angular_cylindrical"] >= - (np.pi / 2))
    assert all(scalar_field.to_be_added["angular_cylindrical"] <= (np.pi * 1.5))

