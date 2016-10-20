#       HAKUNA MATATA

import pandas as pd
from scipy.io import loadmat, savemat


def read_mat(filename):
    """ Read a .mat file and store all possible elements in pandas DataFrame 
    Parameters
    ----------
    filename: str
        Path tho the filename

    Returns
    -------
    data: dict
        If possible, elements as pandas DataFrames else input format
    """
    
    mat = loadmat(filename)

    if "points" in mat:
        columns = None

        if "points_names" in mat:
            columns= [mat["points_names"][i].strip() for i in range(len(mat["points_names"]))]
            del mat["points_names"]
        
        mat["points"] = pd.DataFrame(mat["points"], columns=columns)

        if "points_dtypes" in mat:
            for i in range(len(mat["points_dtypes"])):
                mat["points"][columns[i]] = mat["points"][columns[i]].astype(mat["points_dtypes"][i].strip())
            
            del mat["points_dtypes"]
            
    
    if "mesh" in mat:
        columns = None

        if "mesh_names" in mat:
            columns= [mat["mesh_names"][i].strip() for i in range(len(mat["mesh_names"]))]
            del mat["mesh_names"]
        
        mat["mesh"] = pd.DataFrame(mat["mesh"], columns=columns)

        if "mesh_dtypes" in mat:
            for i in range(len(mat["mesh_dtypes"])):
                mat["mesh"][columns[i]] = mat["mesh"][columns[i]].astype(mat["mesh_dtypes"][i].strip())
            
            del mat["mesh_dtypes"]
            
    return mat


def write_mat(filename,  **kwargs):
    
    """

    Parameters
    ----------
    filename: str
        The created file will be named with this

    kwargs: Elements of the pyntcloud to be saved

    Returns
    -------
    boolean
        True if no problems

    """
    for k in kwargs:
        if isinstance(kwargs[k], pd.DataFrame):
            kwargs[k] = kwargs[k].to_records(index=False)
    
    np.savez_compressed(filename, **kwargs)
    
    return True