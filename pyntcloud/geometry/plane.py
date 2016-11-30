#  HAKUNA MATATA


import numpy as np


def plane_def_by(three_points, equation=False):
    """ Return the the plane defined by 3 points
       
    Parameters
    ----------        
    three_points: (3,3) ndarray
        The x,y,z coordinates corresponding to the 3 points from which we want
        to define the plane. Expected format:
            array([[x1,y1,z1],
                   [x2,y2,z2],
                   [x3,y3,z3]])
    
    equation(Optional) : bool
        Set the oputput plane format:
            If True return the a,b,c,d coefficients of the plane.
            If False(Default) return 1 Point and 1 Normal vector.
            
    Returns
    -------
    a, b, c, d : float
        The coefficients solving the plane equation.
        
    or
    
    point, normal: (3,) ndarray
        The plane defined by 1 Point and 1 Normal vector. With format:
        array([Px,Py,Pz]), array([Nx,Ny,Nz])

    """
    
    #: define 2 vectors
    v1 = three_points[1] - three_points[0]
    v2 = three_points[2] - three_points[0]
    
    #: and 1 point
    point = three_points[2]
    
    #: the normal of the plane is the cross product of the 2 vectors.
    # normalized to obtain an unit normal.
    normal = normalize(cross(v1,v2))
    
    if equation:
        #: a,b,c are the x,y,z values of that normal vector
        a, b, c = normal
        
        #: compute a*x + b*y + c*z which equals -d
        d = - np.dot(normal, point)
        
        return a, b, c, d
        
    else:
        return point, normal
        

@nb.jit(nopython=True)  
def project_on_plane(points, plane_point, plane_normal, return_distances=False):
    """ Return the projected points on the plane defined by plane_point and plane_normal.
    
    Parameters
    ----------        
    points: (N,3) ndarray
        The x,y,z coordinates corresponding to the points which we want to project
        on the given plane. Expected format:
            array([[x1,y1,z1],
                   ...
                   [xn,yn,zn]])
            
    plane_point: (3,) ndarray
        The x,y,z coordinates corresponding to a point which belong to the plane.
        Expected format:
            array([Px,Py,Pz])
    
    plane_normal: (3,) array
        The x,y,z coordinates corresponding to the normal of the plane.
        Expected format:
            array([Nx,Ny,Nz])
            
    Returns
    -------
    proj_points : (N,3) array
        The x,y,z coordinates corresponding to the points projected on the plane.
        
    """

    #: just in case
    plane_normal = normalize(plane_normal)
        
    #: get vectors from the plane's point to all the given test points
    vectors = array_minus_vector(points, plane_point)
    
    #: get the scalar projection of the vectors onto the plane's normal
    scalars = np.dot(vectors, plane_normal)
    
    #: get the orthogonal-projection vectors
    orthogonal_projection = scalars_dot_vector(scalars, plane_normal)
    
    #: substract the projections to each point
    proj_points = points - orthogonal_projection
    
    if return_distances:
        return proj_points, norm_all(orthogonal_projection)
    else:
        return proj_points    
        
    
def best_fitting_plane(points, equation=False):
    """ Computes the best fitting plane of the given points
    
    Parameters
    ----------        
    points: array
        The x,y,z coordinates corresponding to the points from which we want
        to define the best fitting plane. Expected format:
            array([
            [x1,y1,z1],
            ...,
            [xn,yn,zn]])
            
    equation(Optional) : bool
            Set the oputput plane format:
                If True return the a,b,c,d coefficients of the plane.
                If False(Default) return 1 Point and 1 Normal vector.    
    Returns
    -------
    a, b, c, d : float
        The coefficients solving the plane equation.
    
    or
    
    point, normal: array
        The plane defined by 1 Point and 1 Normal vector. With format:
        array([Px,Py,Pz]), array([Nx,Ny,Nz])
        
    """
    #: compute PCA 
    w, v = PCA(points)
    
    #: the normal of the plane is the last eigenvector
    normal = normalize(v[:,2])
       
    #: get a point from the plane
    point = np.mean(points, axis=0)
    
    #: if equation == True, return the a,b,c,d coefficients
    if equation:
        #: get A,B,C
        a, b, c = normal
        
        #: get D
        d = -(np.dot(normal, point))
        return a, b, c, d
        
    #: else return the plane as a point and normal 
    else:
        return point, normal        

