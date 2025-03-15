import pytest

import numpy as np

from pyntcloud.scalar_fields.normals import (
    InclinationDegrees,
    InclinationRadians,
    OrientationDegrees,
    OrientationRadians,
)


@pytest.mark.parametrize(
    "scalar_field_class, min_val, max_val",
    [
        (InclinationDegrees, 0, 180),
        (InclinationRadians, 0, np.pi),
        (OrientationDegrees, 0, 360),
        (OrientationRadians, 0, np.pi * 2),
    ],
)
@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_NormalsScalarFields_bounds(
    pyntcloud_with_rgb_and_normals, scalar_field_class, min_val, max_val
):
    cloud = pyntcloud_with_rgb_and_normals
    scalar_field = scalar_field_class(pyntcloud=cloud)
    scalar_field.extract_info()
    with np.errstate(divide="ignore", invalid="ignore"):
        scalar_field.compute()
    scalar_field_values = next(iter(scalar_field.to_be_added.values()))
    assert all(scalar_field_values >= min_val)
    assert all(scalar_field_values <= max_val)
