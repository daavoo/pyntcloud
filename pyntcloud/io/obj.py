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
    comments = []
    obj_info = []
    v = []
    vn = []
    f = []
    
    with open(filename) as obj:
        for line in obj:
            
            if line.startswith('#'):
                if line.startswith('#obj_info'):
                    obj_info.append(line.strip()[1:])
                else:
                    comments.append(line.strip()[1:])
                
            elif line.startswith('v '):
                v.append(line.strip()[1:].split())
                
            elif line.startswith('vn'):
                vn.append(line.strip()[2:].split())
                
            elif line.startswith('f'):
                f.append(line.strip()[2:])
                
                
    v = pd.DataFrame(v, dtype='f4', columns=['x', 'y', 'z'])
    vn = pd.DataFrame(vn, dtype='f4', columns=['nx', 'ny', 'nz'])
    vertex = pd.concat([v, vn], axis=1)
    
    if "//" in f[0]:
        face_columns = ['v1', 'vn1', 'v2', 'vn2', 'v3', 'vn3']
    elif len(vn) > 0:
        face_columns = ['v1', 'vt1', 'vn1', 'v2', 'vt2', 'vn2', 'v3', 'vt3', 'vn3']
    else:
        face_columns = ['v1', 'vt1', 'v2', 'vt2', 'v3', 'vt3']
    
    f = [re.split(r'\D+', x) for x in f]
    
    face = pd.DataFrame(f, dtype='i4', columns=face_columns)
    
    data = {'comments': comments, 'obj_info': obj_info, 'vertex': vertex, 'face': face}
    
    return data
            

def write_obj(filename, vertex=None, face=None, comments=None, obj_info=None):
    """
    Parameters
    ----------
    filename:   str
        The created file will be named with this
    vertex:     pd.DataFrame
    face:       pd.DataFrame
    comments:   list[str] or str
    obj_info:   list[str] or str

    Returns
    -------
    boolean
        True if no problems

    """     
    if not filename.endswith('obj'):
        filename += '.obj'

    with open(filename, "w") as obj:

        for line in comments:
            obj.write("#%s\n" % line.strip())

        for line in obj_info:
            obj.write("#%s\n" % line.strip())

    if vertex is not None:
        # because we don't want the insert on the original data
        vertex = vertex.copy()
        vertex.insert(loc=0, column="obj_v", value="v")
        vertex.to_csv(filename, sep=" ", index=False, header=False, mode='a',
                                                                encoding='ascii')
                                                                                        
    return True
            

            
                
