import pytest

import numpy as np


@pytest.mark.parametrize("scalar_field_name, min_val, max_val", [
    (
        "inclination_degrees",
        0,
        180
    ),
    (
        "inclination_radians",
        0,
        np.pi
    ),
    (
        "orientation_degrees",
        0,
        360
    ),
    (
        "orientation_radians",
        0,
        np.pi * 2
    ),
])
@pytest.mark.usefixtures("pyntcloud_with_rgb_and_normals")
def test_normal_scalar_fields_bounds(pyntcloud_with_rgb_and_normals, scalar_field_name, min_val, max_val):
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field = pyntcloud_with_rgb_and_normals.add_scalar_field(
            scalar_field_name)

    scalar_field_values = pyntcloud_with_rgb_and_normals.points[scalar_field]
    assert all(scalar_field_values >= min_val)
    assert all(scalar_field_values <= max_val)
