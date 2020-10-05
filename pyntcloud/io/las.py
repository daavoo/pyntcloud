try:
    import laspy
except ImportError:
    laspy = None
import pandas as pd


def convert_location_to_dtype(data, dtype_str):
    data["points"] = data["points"].astype({"x": dtype_str, "y": dtype_str, "z": dtype_str})
    return data


def get_color_dtype(data, column_names):
    color_data_types = [data["points"][column_name].dtype for column_name in column_names]
    assert len(set(color_data_types)) == 1
    return color_data_types[0]


def convert_color_to_dtype(data, output_dtype):
    assert output_dtype in ["uint8", "uint16"]
    column_names = ["red", "green", "blue"]
    input_dtype = get_color_dtype(data, column_names)
    # Color information in las/laz files is stored as uint8 or uint16
    assert input_dtype in ["uint8", "uint16"]
    if input_dtype == "uint8" and output_dtype == "uint16":
        data["points"].loc[:, column_names] *= 256
    elif input_dtype == "uint16" and output_dtype == "uint8":
        data["points"].loc[:, column_names] /= 256
    data["points"] = data["points"].astype({"red": output_dtype, "green": output_dtype, "blue": output_dtype})
    return data


def read_las(filename, xyz_dtype="float32", rgb_dtype="uint8"):
    """Read a .las/laz file and store elements in pandas DataFrame.

    Parameters
    ----------
    filename: str
        Path to the filename
    xyz_dtype: str
        Defines the data type of the xyz coordinate
    rgb_dtype: str
        Defines the data type of the color
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
        data = convert_location_to_dtype(data, xyz_dtype)
        data = convert_color_to_dtype(data, rgb_dtype)
        data["las_header"] = las.header

    return data
