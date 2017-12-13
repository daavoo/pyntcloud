import os
import shutil
from pathlib import Path
import json
try:
    from IPython.display import IFrame
except ImportError:
    IFrame = None


def plot_PyntCloud(cloud, point_size=0.3, output_name="pyntcloud_plot", width=800, height=500):
    """ Generate 3 output files (html, json and ply) to be plotted in Jupyter

    Parameters
    ----------
    cloud: PyntCloud instance

    point_size: float, optional
        Default: 0.3
        Size of the plotted points.

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

    return IFrame("{}.html".format(output_name), width=width, height=height)
