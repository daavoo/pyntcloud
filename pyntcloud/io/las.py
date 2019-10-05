try:
    import laspy
except ImportError:
    laspy = None
import pandas as pd


def read_las(filename):
    """Read a .las/laz file and store elements in pandas DataFrame.

    Parameters
    ----------
    filename: str
        Path to the filename
    Returns
    -------
    data: dict
        Elements as pandas DataFrames.
    """
    if laspy is None:
        raise ImportError("laspy is needed for reading .las files.")
    data = {}

    with laspy.file.File(filename) as las:
        data["points"] = pd.DataFrame(las.points["point"])
        data["points"].columns = (x.lower() for x in data["points"].columns)
        # because laspy do something strange with scale
        data["points"].loc[:, ["x", "y", "z"]] *= las.header.scale
        data["las_header"] = las.header

    return data
