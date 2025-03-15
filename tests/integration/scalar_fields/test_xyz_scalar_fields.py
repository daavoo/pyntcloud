import pytest

import numpy as np


@pytest.mark.usefixtures("plane_pyntcloud")
def test_plane_fit_max_dist(plane_pyntcloud):
    with np.errstate(divide="ignore", invalid="ignore"):
        plane_pyntcloud.add_scalar_field("plane_fit")
    assert sum(plane_pyntcloud.points["is_plane"]) == 4

    with np.errstate(divide="ignore", invalid="ignore"):
        plane_pyntcloud.add_scalar_field("plane_fit", max_dist=0.4)
    assert sum(plane_pyntcloud.points["is_plane"]) == 5


@pytest.mark.usefixtures("sphere_pyntcloud")
def test_sphere_fit_max_dist(sphere_pyntcloud):
    with np.errstate(divide="ignore", invalid="ignore"):
        sphere_pyntcloud.add_scalar_field("sphere_fit")
    assert sum(sphere_pyntcloud.points["is_sphere"]) == 4

    with np.errstate(divide="ignore", invalid="ignore"):
        sphere_pyntcloud.add_scalar_field("sphere_fit", max_dist=0.5)
    assert sum(sphere_pyntcloud.points["is_sphere"]) == 5


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_spherical_coords_bounds(pyntcloud_with_rgb_and_normals):
    with np.errstate(divide="ignore", invalid="ignore"):
        pyntcloud_with_rgb_and_normals.add_scalar_field("spherical_coords")
    assert all(pyntcloud_with_rgb_and_normals.points["polar"] >= 0)
    assert all(pyntcloud_with_rgb_and_normals.points["polar"] <= 180)

    assert all(pyntcloud_with_rgb_and_normals.points["azimuthal"] >= -180)
    assert all(pyntcloud_with_rgb_and_normals.points["azimuthal"] <= 180)

    with np.errstate(divide="ignore", invalid="ignore"):
        pyntcloud_with_rgb_and_normals.add_scalar_field(
            "spherical_coords", degrees=False
        )

    assert all(pyntcloud_with_rgb_and_normals.points["polar"] >= 0)
    assert all(pyntcloud_with_rgb_and_normals.points["polar"] <= np.pi)

    assert all(pyntcloud_with_rgb_and_normals.points["azimuthal"] >= -np.pi)
    assert all(pyntcloud_with_rgb_and_normals.points["azimuthal"] <= np.pi)


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_cylindrical_coords_bounds(pyntcloud_with_rgb_and_normals):
    with np.errstate(divide="ignore", invalid="ignore"):
        pyntcloud_with_rgb_and_normals.add_scalar_field("cylindrical_coords")
    assert all(pyntcloud_with_rgb_and_normals.points["angular_cylindrical"] >= -90)
    assert all(pyntcloud_with_rgb_and_normals.points["angular_cylindrical"] <= 270)

    with np.errstate(divide="ignore", invalid="ignore"):
        pyntcloud_with_rgb_and_normals.add_scalar_field(
            "cylindrical_coords", degrees=False
        )
    assert all(
        pyntcloud_with_rgb_and_normals.points["angular_cylindrical"] >= -(np.pi / 2)
    )
    assert all(
        pyntcloud_with_rgb_and_normals.points["angular_cylindrical"] <= (np.pi * 1.5)
    )
