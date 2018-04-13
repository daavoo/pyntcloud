import pytest

import numpy as np

@pytest.mark.parametrize("scalar_field_name", [
    "anisotropy",
    "planarity"
])
@pytest.mark.usefixtures("pyntcloud_and_eigenvalues")
def test_eigen_values_scalar_fields_where_coplanar_points_have_value_of_1(pyntcloud_and_eigenvalues, scalar_field_name):
    cloud, ev = pyntcloud_and_eigenvalues
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field = cloud.add_scalar_field(
            scalar_field_name,
            ev=ev)
    scalar_field_values = cloud.points[scalar_field].values
    assert all(scalar_field_values[:5] == 1)
    assert scalar_field_values[5] < 1


@pytest.mark.parametrize("scalar_field_name", [
    "curvature",
    "eigenentropy",
    "linearity",
    "omnivariance",
    "sphericity"
])
@pytest.mark.usefixtures("pyntcloud_and_eigenvalues")
def test_eigen_values_scalar_fieldss_where_coplanar_points_have_value_of_0(pyntcloud_and_eigenvalues, scalar_field_name):
    cloud, ev = pyntcloud_and_eigenvalues
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field = cloud.add_scalar_field(
            scalar_field_name,
            ev=ev)
    scalar_field_values = cloud.points[scalar_field].values
    assert all(scalar_field_values[:5] == 0)
    assert scalar_field_values[5] > 0


@pytest.mark.usefixtures("pyntcloud_and_eigenvalues")
def test_eigen_sum_values(pyntcloud_and_eigenvalues):
    cloud, ev = pyntcloud_and_eigenvalues
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field = cloud.add_scalar_field(
            "eigen_sum",
            ev=ev)
    scalar_field_values = cloud.points[scalar_field].values
    assert all(scalar_field_values > 0)



