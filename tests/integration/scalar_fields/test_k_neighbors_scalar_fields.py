import pytest

import numpy as np


@pytest.mark.usefixtures("plane_pyntcloud", "plane_k_neighbors")
def test_eigen_values_coplanar_points_e3_is_0(plane_pyntcloud, plane_k_neighbors):
    plane_pyntcloud.add_scalar_field(
        "eigen_values",
        k_neighbors=plane_k_neighbors)
    assert plane_pyntcloud.points["e3(3)"][2] == 0
    assert plane_pyntcloud.points["e3(3)"][3] == 0


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals", "pyntcloud_with_rgb_and_normals_k_neighbors")
def test_eigen_values_bounds(pyntcloud_with_rgb_and_normals, pyntcloud_with_rgb_and_normals_k_neighbors):
    scalar_fields = pyntcloud_with_rgb_and_normals.add_scalar_field(
        "eigen_values",
        k_neighbors=pyntcloud_with_rgb_and_normals_k_neighbors)

    for x in scalar_fields:
        assert all(pyntcloud_with_rgb_and_normals.points[x] >= -1)
        assert all(pyntcloud_with_rgb_and_normals.points[x] <= 1)


@pytest.mark.usefixtures("plane_pyntcloud", "plane_k_neighbors")
def test_eigen_decomposition_coplanar_points_some_fields_are_0(plane_pyntcloud, plane_k_neighbors):
    plane_pyntcloud.add_scalar_field(
        "eigen_decomposition",
        k_neighbors=plane_k_neighbors)

    for x in [
        "e3(3)",
        "ev1_z(3)",
        "ev2_z(3)",
        "ev3_x(3)",
        "ev3_y(3)"
    ]:
        assert plane_pyntcloud.points[x][2] == 0
        assert plane_pyntcloud.points[x][3] == 0


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals", "pyntcloud_with_rgb_and_normals_k_neighbors")
def test_eigen_decomposition_bounds(pyntcloud_with_rgb_and_normals, pyntcloud_with_rgb_and_normals_k_neighbors):
    scalar_fields = pyntcloud_with_rgb_and_normals.add_scalar_field(
        "eigen_decomposition",
        k_neighbors=pyntcloud_with_rgb_and_normals_k_neighbors)

    for x in scalar_fields:
        assert all(pyntcloud_with_rgb_and_normals.points[x] >= -1)
        assert all(pyntcloud_with_rgb_and_normals.points[x] <= 1)


@pytest.mark.usefixtures("plane_pyntcloud", "plane_k_neighbors")
def test_normals_coplanar_points_nx_ny_are_0(plane_pyntcloud, plane_k_neighbors):
    plane_pyntcloud.add_scalar_field(
        "normals",
        k_neighbors=plane_k_neighbors)
    for x in ["nx(3)", "ny(3)"]:
        assert plane_pyntcloud.points[x][2] == 0
        assert plane_pyntcloud.points[x][3] == 0


@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals", "pyntcloud_with_rgb_and_normals_k_neighbors")
def test_normals_bounds(pyntcloud_with_rgb_and_normals, pyntcloud_with_rgb_and_normals_k_neighbors):
    scalar_fields = pyntcloud_with_rgb_and_normals.add_scalar_field(
        "normals",
        k_neighbors=pyntcloud_with_rgb_and_normals_k_neighbors)

    for x in scalar_fields:
        assert all(pyntcloud_with_rgb_and_normals.points[x] >= -1)
        assert all(pyntcloud_with_rgb_and_normals.points[x] <= 1)
