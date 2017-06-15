import numpy as np


def spherical_to_cartesian(radial, azimuthal, polar):
    """
    Convert spherical coordinates (r, theta, phi) to cartesian (x, y, z).

    Parameters
    ----------
    radial: (N,) ndarray
        'r'. Radial distance.
    azimutal: (N,) ndarray
        'theta'. Azimutal angle.
    polar: (N,) ndarray
        'phi'. Polar angle.

    Returns
    -------
    xyz: (N, 3) ndarray
        Corresponding cartesian coordiantes.

    Notes
    -----
    Use notation of mathematical systems, NOT physics.
    """
    sin_theta = np.sin(azimuthal)
    cos_theta = np.cos(azimuthal)
    sin_phi = np.sin(polar)
    cos_phi = np.cos(polar)

    xyz = np.empty((radial.shape[0], 3), dtype=np.float32)

    xyz[:, 0] = radial * sin_phi * cos_theta
    xyz[:, 1] = radial * sin_phi * sin_theta
    xyz[:, 2] = radial * cos_phi

    return xyz
