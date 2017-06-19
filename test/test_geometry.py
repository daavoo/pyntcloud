import numpy as np
from pyntcloud.geometry.coord_systems import (
    spherical_to_cartesian,
    cartesian_to_spherical,
    cylindrical_to_cartesian,
    cartesian_to_cylindrical,
)


def test_spherical_to_cartesian():
    expected = np.array([[0.5, 0.5, 0.7071], [0.5, -0.5, -0.7071]])

    data = np.array([[1, 45, 45], [1, -45, 135]], dtype=np.float32)
    result = spherical_to_cartesian(data[:, 0], data[:, 1], data[:, 2])

    assert np.all(np.isclose(result, expected))

    data[:, 1:] = np.deg2rad(data[:, 1:])

    result = spherical_to_cartesian(data[:, 0], data[:, 1], data[:, 2], degrees=False)

    assert np.all(np.isclose(result, expected))


def test_cartesian_to_spherical():
    expected = np.array([[1, 45, 45], [1, -45, 135]], dtype=np.float32)

    data = np.array([[0.5, 0.5, 0.7071], [0.5, -0.5, -0.7071]])

    result = np.zeros_like(expected)
    radial, azimuthal, polar = cartesian_to_spherical(data)
    result[:, 0] = radial
    result[:, 1] = azimuthal
    result[:, 2] = polar

    assert np.all(np.isclose(result, expected))

    expected[:, 1:] = np.deg2rad(expected[:, 1:])

    radial, azimuthal, polar = cartesian_to_spherical(data, degrees=False)
    result[:, 0] = radial
    result[:, 1] = azimuthal
    result[:, 2] = polar

    assert np.all(np.isclose(result, expected))


def test_cylindrical_to_cartesian():
    expected = np.array([[0.5, 0.5, 0.7071], [0.5, -0.5, -0.7071]])

    data = np.array([[0.7071, 45, 0.7071], [0.7071, -45, -0.7071]], dtype=np.float32)
    result = cylindrical_to_cartesian(data[:, 0], data[:, 1], data[:, 2])

    assert np.all(np.isclose(result, expected))

    data[:, 1] = np.deg2rad(data[:, 1])

    result = cylindrical_to_cartesian(data[:, 0], data[:, 1], data[:, 2], degrees=False)

    assert np.all(np.isclose(result, expected))


def test_cartesian_to_cylindrical():
    expected = np.array([[0.7071, 45, 0.7071], [0.7071, -45, -0.7071]], dtype=np.float32)

    data = np.array([[0.5, 0.5, 0.7071], [0.5, -0.5, -0.7071]])

    result = np.zeros_like(expected)
    radial, angular, height = cartesian_to_cylindrical(data)
    result[:, 0] = radial
    result[:, 1] = angular
    result[:, 2] = height

    assert np.all(np.isclose(result, expected))

    expected[:, 1] = np.deg2rad(expected[:, 1])

    radial, angular, height = cartesian_to_cylindrical(data, degrees=False)
    result[:, 0] = radial
    result[:, 1] = angular
    result[:, 2] = height

    assert np.all(np.isclose(result, expected))
