import pytest

import numpy as np

from pyntcloud.scalar_fields.k_neighbors import (
    EigenValues,
    EigenDecomposition,
    UnorientedNormals,
)


@pytest.mark.parametrize(
    "ScalarField", [EigenValues, EigenDecomposition, UnorientedNormals]
)
@pytest.mark.usefixtures("plane_pyntcloud", "plane_k_neighbors")
def test_KNeighborsScalarField_adds_self_point_to_neighborhood(
    plane_pyntcloud, plane_k_neighbors, ScalarField
):
    """
    PyntCloud.get_neighbors does not return the index of each point, just the neighbors.
    The index of each point should be added to the neighborhood in order to use it for
    the computation of the scalar field.
    """
    scalar_field = ScalarField(pyntcloud=plane_pyntcloud, k_neighbors=plane_k_neighbors)
    scalar_field.extract_info()
    assert scalar_field.k_neighbors.shape[1] == plane_k_neighbors.shape[1] + 1


@pytest.mark.usefixtures("plane_pyntcloud", "plane_k_neighbors")
def test_EigenValues_coplanar_points_e3_is_0(plane_pyntcloud, plane_k_neighbors):
    scalar_field = EigenValues(pyntcloud=plane_pyntcloud, k_neighbors=plane_k_neighbors)
    scalar_field.extract_info()
    with np.errstate(divide="ignore", invalid="ignore"):
        scalar_field.compute()
    assert scalar_field.to_be_added["e3(3)"][2] == 0
    assert scalar_field.to_be_added["e3(3)"][3] == 0


@pytest.mark.usefixtures(
    "pyntcloud_with_rgb_and_normals", "pyntcloud_with_rgb_and_normals_k_neighbors"
)
def test_EigenValues_bounds(
    pyntcloud_with_rgb_and_normals, pyntcloud_with_rgb_and_normals_k_neighbors
):
    scalar_field = EigenValues(
        pyntcloud=pyntcloud_with_rgb_and_normals,
        k_neighbors=pyntcloud_with_rgb_and_normals_k_neighbors,
    )
    scalar_field.extract_info()
    with np.errstate(divide="ignore", invalid="ignore"):
        scalar_field.compute()

    for x in ["e1(4)", "e2(4)", "e3(4)"]:
        assert all(scalar_field.to_be_added[x] >= -1)
        assert all(scalar_field.to_be_added[x] <= 1)


@pytest.mark.usefixtures("plane_pyntcloud", "plane_k_neighbors")
def test_EigenDecomposition_coplanar_points_some_fields_are_0(
    plane_pyntcloud, plane_k_neighbors
):
    scalar_field = EigenDecomposition(
        pyntcloud=plane_pyntcloud, k_neighbors=plane_k_neighbors
    )
    scalar_field.extract_info()
    with np.errstate(divide="ignore", invalid="ignore"):
        scalar_field.compute()

    for x in ["e3(3)", "ev1_z(3)", "ev2_z(3)", "ev3_x(3)", "ev3_y(3)"]:
        assert scalar_field.to_be_added[x][2] == 0
        assert scalar_field.to_be_added[x][3] == 0


@pytest.mark.usefixtures(
    "pyntcloud_with_rgb_and_normals", "pyntcloud_with_rgb_and_normals_k_neighbors"
)
def test_EigenDecomposition_bounds(
    pyntcloud_with_rgb_and_normals, pyntcloud_with_rgb_and_normals_k_neighbors
):
    scalar_field = EigenDecomposition(
        pyntcloud=pyntcloud_with_rgb_and_normals,
        k_neighbors=pyntcloud_with_rgb_and_normals_k_neighbors,
    )
    scalar_field.extract_info()
    with np.errstate(divide="ignore", invalid="ignore"):
        scalar_field.compute()

    for x in [
        "e1(4)",
        "e2(4)",
        "e3(4)",
        "ev1_x(4)",
        "ev1_x(4)",
        "ev1_x(4)",
        "ev2_x(4)",
        "ev2_y(4)",
        "ev2_y(4)",
        "ev3_x(4)",
        "ev3_z(4)",
        "ev3_z(4)",
    ]:
        assert all(scalar_field.to_be_added[x] >= -1)
        assert all(scalar_field.to_be_added[x] <= 1)


@pytest.mark.usefixtures("plane_pyntcloud", "plane_k_neighbors")
def test_UnorientedNormals_coplanar_points_nx_ny_are_0(
    plane_pyntcloud, plane_k_neighbors
):
    scalar_field = UnorientedNormals(
        pyntcloud=plane_pyntcloud, k_neighbors=plane_k_neighbors
    )
    scalar_field.extract_info()
    with np.errstate(divide="ignore", invalid="ignore"):
        scalar_field.compute()
    for x in ["nx(3)", "ny(3)"]:
        assert scalar_field.to_be_added[x][2] == 0
        assert scalar_field.to_be_added[x][3] == 0


@pytest.mark.usefixtures(
    "pyntcloud_with_rgb_and_normals", "pyntcloud_with_rgb_and_normals_k_neighbors"
)
def test_UnorientedNormals_bounds(
    pyntcloud_with_rgb_and_normals, pyntcloud_with_rgb_and_normals_k_neighbors
):
    scalar_field = UnorientedNormals(
        pyntcloud=pyntcloud_with_rgb_and_normals,
        k_neighbors=pyntcloud_with_rgb_and_normals_k_neighbors,
    )
    scalar_field.extract_info()
    with np.errstate(divide="ignore", invalid="ignore"):
        scalar_field.compute()

    for x in ["nx(4)", "ny(4)", "nz(4)"]:
        assert all(scalar_field.to_be_added[x] >= -1)
        assert all(scalar_field.to_be_added[x] <= 1)
