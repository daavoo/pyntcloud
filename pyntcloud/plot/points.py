import os
import json
from IPython.display import IFrame


def plot_PyntCloud(cloud, output_name="pyntcloud_plot", width=800, height=500):
    """ Generate 3 output files (html, json and ply) to be plotted in Jupyter

    Parameters
    ----------
    cloud: PyntCloud instance
    """

    src = "{}/{}".format(os.path.dirname(os.path.abspath(__file__)), "points.html")
    dst = "{}/{}".format(os.getcwd(), "{}.html".format(output_name))

    # write new html file replacing placeholder
    with open(src, "r") as inp, open(dst, "w") as out:
        for line in inp:
            if "FILENAME_PLACEHOLDER" in line:
                line = line.replace("FILENAME_PLACEHOLDER", "'{}'".format(output_name))

            out.write(line)

    conf = {}
    conf["camera_position"] = (cloud.xyz.max(0) + abs(cloud.xyz.max(0))).tolist()
    conf["look_at"] = cloud.xyz.mean(0).tolist()

    with open("{}.json".format(output_name), "w") as json_out_file:
        json.dump(conf, json_out_file)

    cloud.to_file("{}.ply".format(output_name))

    return IFrame("{}.html".format(output_name), width=width, height=height)
