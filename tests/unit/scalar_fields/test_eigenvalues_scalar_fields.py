import pytest

import numpy as np

from pyntcloud.scalar_fields.eigenvalues import (
    Anisotropy,
    Curvature,
    Eigenentropy,
    EigenSum,
    Linearity,
    Omnivariance,
    Planarity,
    Sphericity
)


@pytest.mark.parametrize("scalar_field_class", [
    Anisotropy,
    Planarity
])
@pytest.mark.usefixtures("pyntcloud_and_eigenvalues")
def test_EigenValuesScalarFields_where_coplanar_points_have_value_of_1(pyntcloud_and_eigenvalues, scalar_field_class):
    cloud, ev = pyntcloud_and_eigenvalues
    scalar_field = scalar_field_class(
        pyntcloud=cloud,
        ev=ev)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    scalar_field_values = next(iter(scalar_field.to_be_added.values()))
    assert all(scalar_field_values[:5] == 1)
    assert scalar_field_values[5] < 1


@pytest.mark.parametrize("scalar_field_class", [
    Curvature,
    Eigenentropy,
    Linearity,
    Omnivariance,
    Sphericity
])
@pytest.mark.usefixtures("pyntcloud_and_eigenvalues")
def test_EigenValuesScalarFields_where_coplanar_points_have_value_of_0(pyntcloud_and_eigenvalues, scalar_field_class):
    cloud, ev = pyntcloud_and_eigenvalues
    scalar_field = scalar_field_class(
        pyntcloud=cloud,
        ev=ev)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    scalar_field_values = next(iter(scalar_field.to_be_added.values()))
    assert all(scalar_field_values[:5] == 0)
    assert scalar_field_values[5] > 0


@pytest.mark.usefixtures("pyntcloud_and_eigenvalues")
def test_EigenSum_values(pyntcloud_and_eigenvalues):
    cloud, ev = pyntcloud_and_eigenvalues
    scalar_field = EigenSum(
        pyntcloud=cloud,
        ev=ev)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    scalar_field_values = next(iter(scalar_field.to_be_added.values()))
    assert all(scalar_field_values > 0)
