#       HAKUNA MATATA

import numpy as np
import pandas as pd


def read_npz(filename):
    """ Read a .npz file and store all possible elements in pandas DataFrame 
    Parameters
    ----------
    filename: str
        Path tho the filename
    Returns
    -------
    data: dict
        If possible, elements as pandas DataFrames else input format
    """
    
    with np.load(filename) as npz:
        data = {}
        for element in npz.files:
            try:
                data[element] =  pd.DataFrame(npz[element])
            except:
                data[element] = npz[element]
    return data


def write_npz(filename,  **kwargs):
    
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