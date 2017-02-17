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
    
    data = loadmat(filename)

    
    if points_columns in data:
        columns = [data[points_columns][i].strip() for i in range(len(data[points_columns]))]
        del data[points_columns]
        
        data[points_name] = pd.DataFrame(data[points_name], columns=columns)            
    
    if mesh_name in data:
        columns = None

        if mesh_columns in data:
            columns= [data[mesh_columns][i].strip() for i in range(len(data[mesh_columns]))]
            del data[mesh_columns]
        
        data[mesh_name] = pd.DataFrame(data[mesh_name], columns=columns)
            
    return data
