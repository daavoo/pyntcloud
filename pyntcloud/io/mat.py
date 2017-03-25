#       HAKUNA MATATA

import pandas as pd
from scipy.io import loadmat


def read_mat(filename, points_name="points", mesh_name="mesh", 
            points_columns="points_columns",
            mesh_columns="mesh_columns",
            points_dtypes="points_dtypes",
            mesh_dtypes="mesh_dtypes"):
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
    else:
        columns = ["x", "y", "z"]
        for i in range(mat[points_name].shape[1] - 3):
            columns.append("sf{}".format(i))
    
    data["points"] = pd.DataFrame(mat[points_name], columns=columns)  
    
    if points_dtypes in mat:
        for i in range(len(mat[points_dtypes])):
            data["points"][columns[i]] = data["points"][columns[i]].astype(mat[points_dtypes][i].strip())          
    
    if mesh_name in mat:
        if mesh_columns in mat:
            columns= [mat[mesh_columns][i].strip() for i in range(len(mat[mesh_columns]))]
            data["mesh"] = pd.DataFrame(mat[mesh_name], columns=columns)
        else:
            columns = ["v1", "v2", "v3"]
            for i in range(mat[mesh_name].shape[1] - 3):
                columns.append("sf{}".format(i))
        data["mesh"] = pd.DataFrame(mat[mesh_name], columns=columns)

        if mesh_dtypes in mat:
            for i in range(len(mat[mesh_dtypes])):
                data["mesh"][columns[i]] = data["mesh"][columns[i]].astype(mat[mesh_dtypes][i].strip())     

            
    return data
