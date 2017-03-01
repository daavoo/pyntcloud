
import numpy as np

def inclination_deg(normals):
    """ Vertical inclination with respect to Z axis in degrees.

    Parameters
    ----------
    normals: (N, 3) ndarray
        The normal vector associated to each of the 'N' points defined by 
        it's nx, ny, nz components.
    
    Returns
    -------
    inclination_deg: (N,) ndarray
        The inclination angle in degrees associated to each of the 'N' points.
    """
    
    return [np.rad2deg(np.arccos(normals[:,-1]))]

def inclination_rad(normals):
    """ Vertical inclination with respect to Z axis in radians.

    Parameters
    ----------
    normals: (N, 3) ndarray
        The normal vector associated to each of the 'N' points defined by 
        it's nx, ny, nz components.
    
    Returns
    -------
    inclination_rad: (N,) ndarray
        The inclination angle in radians associated to each of the 'N' points.
    """

    return [np.arccos(normals[:,-1])]

def orientation_deg(normals):
    """ Horizontal orientation with respect to the XY plane in degrees.

    Parameters
    ----------
    normals: (N, 3) ndarray
        The normal vector associated to each of the 'N' points defined by 
        it's nx, ny, nz components.
    
    Returns
    -------
    orientation_deg: (N,) ndarray
        The orientation angle in degrees associated to each of the 'N' points.
    """

    angle = np.arctan2(normals[:,0], normals[:,1])
    # convert (-180 , 180) to (0 , 360)
    angle = np.where(angle <0, angle + (2*np.pi), angle)
    return [np.rad2deg(angle)]

def orientation_rad(normals):
    """ Horizontal orientation with respect to the XY plane in radians.

    Parameters
    ----------
    normals: (N, 3) ndarray
        The normal vector associated to each of the 'N' points defined by 
        it's nx, ny, nz components.
    
    Returns
    -------
    orientation_rad: (N,) ndarray
        The orientation angle in radians associated to each of the 'N' points.
    """

    angle = np.arctan2(normals[:,0], normals[:,1])
    # convert (-PI , PI) to (0 , 2*PI)
    angle = np.where(angle <0, angle + (2*np.pi), angle)
    return [angle]