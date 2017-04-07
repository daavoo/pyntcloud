import os
from IPython.display import IFrame
from shutil import copyfile

def plot_points(xyz=None, colors=None, size=0.1, axis=False, output_name=None):
    src = os.path.dirname(os.path.abspath(__file__))
    print(src)
    return
    if output_name is None:
        output_name = "plot_points.html"
        
    positions = xyz.reshape(-1).tolist()

    camera_position = xyz.max(0) + abs(xyz.max(0))

    look = xyz.mean(0)

    if colors is None:
        colors = [1,0.5,0] * len(positions)

    elif len(colors.shape) > 1:
        colors = colors.reshape(-1).tolist()

    if axis:
        size = xyz.ptp() * 1.5
    else:
        axis_size = 0

    
    #copyfile(src, dst)

    return

    return IFrame(output_name, width=800, height=800)


plot_points()


