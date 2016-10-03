#  HAKUNA MATATA

"""
Numba functions
"""

import numpy as np
import numba as nb


@nb.jit(nopython=True)
def array_minus_vector(array, vector):
    
    result = np.zeros(array.shape)
    for i in range(len(array)):
        
        result[i][0] = array[i][0] - vector[0]
        result[i][1] = array[i][1] - vector[1]
        result[i][2] = array[i][2] - vector[2]
    
    return result


@nb.jit(nopython=True)
def scalars_dot_vector(scalars, vector):
    
    result = np.zeros((len(scalars), len(vector)))
    
    for i in range(len(scalars)):
        result[i][0] = scalars[i] * vector[0]
        result[i][1] = scalars[i] * vector[1]
        result[i][2] = scalars[i] * vector[2]
    
    return result

@nb.jit(nopython=True)
def mean_axis0(array_2D):
    
    result = np.zeros(array_2D.shape[1])
    
    for i in range(array_2D.shape[0]):
        for j in range(array_2D.shape[1]):
            result[j] += array_2D[i][j]
    
    for k in range(array_2D.shape[1]):
        result[k] = result[k] / (array_2D.shape[0])
    
    return result
     
    
@nb.jit(nopython=True)
def get_min(one, other):
    
    x = min(one[0], other[0])
    y = min(one[1], other[1])
    z = min(one[2], other[2])
    return np.array([x,y,z])
    

@nb.jit(nopython=True)
def get_max(one, other):
    
    x = max(one[0], other[0])
    y = max(one[1], other[1])
    z = max(one[2], other[2])
    return np.array([x,y,z])


@nb.jit(nopython=True)
def assing_ray(n, xyz, view_point, centroids, min_dist):
    
    origin = xyz[n]
    
    xyzmin = get_min(origin, view_point)
    xyzmax = get_max(origin, view_point)
    
    b = norm(view_point - origin)
    
    for i in range(len(centroids)):
        
        if centroids[i][0] > xyzmin[0] and \
            centroids[i][1] > xyzmin[1] and \
            centroids[i][2] > xyzmin[2] and \
            centroids[i][0] < xyzmax[0] and \
            centroids[i][1] < xyzmax[1] and \
            centroids[i][2] < xyzmax[2]:
                
            a = norm(origin - centroids[i])
            c = norm(view_point - centroids[i])
            s = (a + b + c) / 2
            
            dist = (2 / b) * (np.sqrt( s * (s - a) * (s - b) * (s - c)))
            
            if dist <= min_dist:
                return np.array([np.nan, np.nan, np.nan], dtype=np.float32)
               
    view_ray = view_point- origin
    normalize(view_ray)
    
    return view_ray
    
@nb.jit(nopython=True)
def numba_loop(xyz, view_point, centroids, min_dist):
    
    for n in range(len(xyz)):
        assing_ray(n, xyz, view_point, centroids, min_dist)
        
"""
pd.DataFrame(pool.starmap(assing_ray,zip(range(len(xyz)), repeat(xyz),repeat(view_point), repeat(centroids), repeat(min_dist))))
"""
