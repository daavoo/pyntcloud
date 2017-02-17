#       HAKUNA MATATA

import re
import pandas as pd

def read_obj(filename):
    """ Reads and obj file and return the elements as pandas Dataframes.

    Parameters
    ----------
    filename: str
        Path to the obj file.

    Returns
    -------
    Each obj element found as pandas Dataframe.

    """
    v = []
    vn = []
    f = []
    
    with open(filename) as obj:
        for line in obj:
            if line.startswith('v '):
                v.append(line.strip()[1:].split())
                
            elif line.startswith('vn'):
                vn.append(line.strip()[2:].split())
                
            elif line.startswith('f'):
                f.append(line.strip()[2:])
                
                
    points = pd.DataFrame(v, dtype='f4', columns=['x', 'y', 'z'])
    vn = pd.DataFrame(vn, dtype='f4', columns=['nx', 'ny', 'nz'])
    
    if len(f) > 0 and "//" in f[0]:
        mesh_columns = ['v1', 'vn1', 'v2', 'vn2', 'v3', 'vn3']
    elif len(vn) > 0:
        mesh_columns = ['v1', 'vt1', 'vn1', 'v2', 'vt2', 'vn2', 'v3', 'vt3', 'vn3']
    else:
        mesh_columns = ['v1', 'vt1', 'v2', 'vt2', 'v3', 'vt3']
    
    f = [re.split(r'\D+', x) for x in f]
    
    mesh = pd.DataFrame(f, dtype='i4', columns=mesh_columns)
    
    data = {'points': points, 'mesh': mesh, "normals":vn}
    
    return data
            

def write_obj(filename, points=None, mesh=None):
    """
    Parameters
    ----------
    filename:   str
        The created file will be named with this
    points:     pd.DataFrame
    mesh:       pd.DataFrame

    Returns
    -------
    boolean
        True if no problems

    """     
    if not filename.endswith('obj'):
        filename += '.obj'

    if points is not None:
        # because we don't want the insert on the original data
        points = points.copy()
        points = points[["x", "y", "z"]]
        points.insert(loc=0, column="obj_v", value="v")
        points.to_csv(filename, sep=" ", index=False, header=False, mode='a',
                                                                encoding='ascii')
    
    #if mesh is not None:

                                                                                        
    return True
            

            
                
