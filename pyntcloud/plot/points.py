import os
from IPython.display import IFrame


def plot_PyntCloud(cloud, output_name="pyntcloud_plot", width=800, height=500):
    """ Generate 3 output files (html, json and ply) to be plotted in Jupyter

    Parameters
    ----------
    cloud: PyntCloud instance
    """

    src = "{}/{}".format(os.path.dirname(os.path.abspath(__file__)), "points.html")
    dst = "{}/{}".format(os.getcwd(), "{}.html".format(output_name))

    camera_position = (cloud.xyz.max(0) + abs(cloud.xyz.max(0))).tolist()
    look_at = cloud.xyz.mean(0).tolist()

    # write new html file replacing placeholder
    with open(src, "r") as inp, open(dst, "w") as out:
        for line in inp:
            if "FILENAME_PLACEHOLDER" in line:
                line = line.replace("FILENAME_PLACEHOLDER", "'{}'".format(output_name))

            elif "CAMERA_POSITION_PLACEHOLDER" in line:
                line = line.replace("CAMERA_POSITION_PLACEHOLDER", "{}".format(camera_position))

            elif "LOOK_AT_PLACEHOLDER" in line:
                line = line.replace("LOOK_AT_PLACEHOLDER", "{}".format(look_at))

            out.write(line)

    cloud.to_file("{}.ply".format(output_name))

    return IFrame("{}.html".format(output_name), width=width, height=height)
