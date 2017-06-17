import numpy as np


def spherical_to_cartesian(radial, azimuthal, polar, degrees=True):
    """
    Convert spherical coordinates (r, theta, phi) to cartesian (x, y, z).

    Parameters
    ----------
    radial: (N,) ndarray
        'r'. Radial distance.
    azimuthal: (N,) ndarray
        'theta'. Azimuthal angle.
    polar: (N,) ndarray
        'phi'. Polar angle.
    degrees: bool, optional
        If True, azimuthal and polar will be assumed to be in degrees.

    Returns
    -------
    xyz: (N, 3) ndarray
        Corresponding cartesian coordiantes.

    Notes
    -----
    Use notation of mathematical systems, NOT physics.
    """
    if degrees:
        azimuthal = np.deg2rad(azimuthal)
        polar = np.deg2rad(polar)

    sin_theta = np.sin(azimuthal)
    cos_theta = np.cos(azimuthal)
    sin_phi = np.sin(polar)
    cos_phi = np.cos(polar)

    xyz = np.empty((radial.shape[0], 3), dtype=np.float32)

    xyz[:, 0] = radial * sin_phi * cos_theta
    xyz[:, 1] = radial * sin_phi * sin_theta
    xyz[:, 2] = radial * cos_phi

    return xyz


def cartesian_to_spherical(xyz, degrees=True):
    """
    Convert cartesian coordinates (x, y, z) to spherical (r, theta, phi).

    Parameters
    ----------
    xyz: (N, 3) ndarray
        Corresponding cartesian coordiantes.
    degrees: bool, optional
        If True, azimuthal and polar will be returned in degrees.

    Returns
    -------
    radial: (N,) ndarray
        'r'. Radial distance.
    azimuthal: (N,) ndarray
        'theta'. Azimuthal angle.
    polar: (N,) ndarray
        'phi'. Polar angle.

    Notes
    -----
    Use notation of mathematical systems, NOT physics.
    """
    x = xyz[:, 0]
    y = xyz[:, 1]
    z = xyz[:, 2]

    radial = np.sqrt((x * x) + (y * y) + (z * z))

    azimuthal = np.arctan(y / x)

    polar = np.arccos(z / radial)

    if degrees:
        azimuthal = np.rad2deg(azimuthal)
        polar = np.rad2deg(polar)

    return radial, azimuthal, polar
