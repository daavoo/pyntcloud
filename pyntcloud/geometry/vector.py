#  HAKUNA MATATA

"""
Vector functions

"""

import numpy as np
import numba as nb


@nb.jit(nopython=True)  
def norm(vector):
    """ Return the lenght(norm) of the vector.
    
    Parameters
    ----------        
    vector: (3,) ndarray
        The input vector. Expected format: 
            array([xi,yi,zi])
       
    Returns
    -------
    norm : float
        The lenght(norm) of the vector.       
    """
    return np.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)


@nb.jit(nopython=True) 
def norm_all(array_of_vectors):
    
    result = np.zeros(len(array_of_vectors))
    
    for i in range(len(array_of_vectors)):
        
        result[i] = norm(array_of_vectors[i])
        
    return result
        
@nb.jit(nopython=True) 
def normalize(vector):
    """ Return the normalized vector.
    
    Parameters
    ----------        
    vector: (3,) ndarray
        The input vector. Expected format: 
            array([xi,yi,zi])
            
    Returns
    -------
    vector : (3,) ndarray
        The normalized vector.      
    """
    vector_norm = norm(vector)
    
    #: to avoid divide by zero error
    if vector_norm < 1e-6:
        vector[0] = 0
        vector[1] = 0
        vector[2] = 0
        
    else:
        vector[0] = vector[0] / vector_norm
        vector[1] = vector[1] / vector_norm
        vector[2] = vector[2] / vector_norm
    
    return vector
    
    
@nb.jit(nopython=True)
def cross(one_vector, other_vector):
    """ Return the cross product between one_vector and other_vector.
    
    Parameters
    ----------        
    one_vector, other_vector: (3,) ndarray
        The input vectors. Expected format: 
            array([xi,yi,zi])
    """
    return np.array([one_vector[1] * other_vector[2] - one_vector[2] * other_vector[1],
                     one_vector[2] * other_vector[0] - one_vector[0] * other_vector[2],
                     one_vector[0] * other_vector[1] - one_vector[1] * other_vector[0]])

@nb.jit(nopython=True)
def angle_btwn(one_vector, other_vector, degrees=True):
    """ Computes the angle between vectors v1 and v2   
    
    Parameters
    ----------        
    one_vector, other_vector: (3,) ndarray
        The input vectors. Expected format: 
            array([xi,yi,zi])
        
    degrees(Optional) : bool
            Set the oputput orientation units:
                If True(Default) set units to degrees.
                If False set units to radians.
    
    Returns
    -------
    angle : float
        The angle between the given vectors.
        
    """
    
    one_vector = normalize(one_vector)
    other_vector = normalize(other_vector)
    
    angle = np.arccos(np.dot(one_vector, other_vector))
    
    if degrees:
        return angle * 180 / np.pi
        
    else:
        return angle