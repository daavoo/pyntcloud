import numpy as np
from pyntcloud.geometry.coord_systems import (
    spherical_to_cartesian,
    cartesian_to_spherical
)


def test_spherical_to_cartesian():
    expected = np.array([[0.5, 0.5, 0.7071], [0.5, -0.5, -0.7071]])

    data = np.array([[1, 45, 45], [-1, -45, -45]], dtype=np.float32)
    result = spherical_to_cartesian(data[:, 0], data[:, 1], data[:, 2])

    assert np.all(np.isclose(result, expected))

    data[:, 1:] = np.deg2rad(data[:, 1:])

    result = spherical_to_cartesian(data[:, 0], data[:, 1], data[:, 2], degrees=False)

    assert np.all(np.isclose(result, expected))
