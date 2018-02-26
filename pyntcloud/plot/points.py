import os
import shutil
from pathlib import Path
import json

import numpy as np

try:
    from IPython.display import IFrame
except ImportError:
    IFrame = None


def plot_PyntCloud(cloud,
    point_size=0.3, 
    point_opacity=0.9,
    output_name="pyntcloud_plot",
    IFrame_shape=(800, 500), 
    polylines={}
    ):
    """ Generate 3 output files (html, json and ply) to be plotted in Jupyter

    Parameters
    ----------
    cloud: PyntCloud instance
    point_size: float, optional
        Default 0.3.
        Size of the points. I don't know what the number means. Check three.js docs.
    point_opacity: float, optional
        Default 0.9.
        0 transparent.
        1 opaque.        
    output_name: str, optional
        Default 'pyntcloud_plot'.
        A standalone output_name.html will be generated.
    IFrame_shape: tuple of ints, optional
        Default (800, 500)
        (Width, Height) of the IFrame rendered in the notebook.
    polylines: dict, optional
        Default {}.
        Mapping hexadecimal colors to a list of list(len(3)) representing the points of the polyline.
        Example:
        polylines={
            "0xFFFFFF": [[0, 0, 0], [0, 0, 1]],
            "0xFF00FF": [[1, 0, 0], [1, 0, 1], [1, 1, 1]]
        }
    """
    if IFrame is None:
        raise ImportError("IFrame is needed for plotting.")

    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    src = "{}/{}".format(BASE_PATH, "points.html")
    dst = "{}/{}".format(os.getcwd(), "{}.html".format(output_name))

    camera_position = (cloud.xyz.max(0) + abs(cloud.xyz.max(0))).tolist()
    look_at = cloud.xyz.mean(0).tolist()

    dest_directory = Path(os.getcwd())
    config_file_path = dest_directory / (output_name + '.config.json')

    config_obj = {
        "filename": output_name,
        "camera_position": camera_position,
        "look_at": look_at,
        "point_size": point_size,
        "point_opacity": point_opacity,
        "polylines_points": list(polylines.values()),
        "polylines_colors": list(polylines.keys()),
    }

    with config_file_path.open('w') as config_file:
        json.dump(config_obj, config_file)

    # write new html file replacing placeholder
    with open(src, "r") as inp, open(dst, "w") as out:
        for line in inp:
            if "FILENAME_PLACEHOLDER" in line:
                line = line.replace("FILENAME_PLACEHOLDER",
                                    "'{}'".format(output_name))
            out.write(line)

    cloud.to_file("{}.ply".format(output_name), also_save=["mesh"])

    try:
        shutil.copytree("{}/assets".format(BASE_PATH),
                        "{}/{}".format(os.getcwd(), "pyntcloud_plot_assets"))
    except FileExistsError:
        pass

    return IFrame("{}.html".format(output_name), width=IFrame_shape[0], height=IFrame_shape[1])
