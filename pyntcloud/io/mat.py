#       HAKUNA MATATA

import pandas as pd
from scipy.io import loadmat, savemat


def read_mat(filename, points_name="points", mesh_name="mesh", 
            points_columns="points_columns",
            mesh_columns="mesh_columns"):
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

    data = {}

    mat = loadmat(filename)

    if points_columns in mat:
        columns = [mat[points_columns][i].strip() for i in range(len(mat[points_columns]))]
        data["points"] = pd.DataFrame(mat[points_name], columns=columns)            
    
    if mesh_name in mat:
        columns = None
        if mesh_columns in mat:
            columns= [mat[mesh_columns][i].strip() for i in range(len(mat[mesh_columns]))]
        data["mesh"] = pd.DataFrame(mat[mesh_name], columns=columns)
            
    return data
