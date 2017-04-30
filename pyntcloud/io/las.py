import laspy
import pandas as pd


def read_las(filename):
    """ Read a .las/laz file and store elements in pandas DataFrame
    Parameters
    ----------
    filename: str
        Path tho the filename
    Returns
    -------
    data: dict
        Elements as pandas DataFrames.
    """

    data = {}

    with laspy.file.File(filename) as las:
        data["points"] = pd.DataFrame(las.points)

    return data
