import pandas as pd


def read_ascii(filename, **kwargs):
    """ Read an ascii file and store elements in pandas DataFrame
    Parameters
    ----------
    filename: str
        Path tho the filename
    kwargs: pandas.read_csv supported kwargs
        Check pandas documentation for all possibilities.
    Returns
    -------
    data: dict
        Elements as pandas DataFrames.
    """

    data = {}

    data["points"] = pd.read_csv(filename, **kwargs)

    return data
