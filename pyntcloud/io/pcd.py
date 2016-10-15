#       HAKUNA MATATA

import sys
import numpy as np
import pandas as pd

byteorder = {"big": ">", "little": "<" }
byteorder = byteorder[sys.byteorder]

def read_pcd(filename):
    """ Reads and pcd file and return the elements as pandas Dataframes.

    Parameters
    ----------
    filename: str
        Path to the pcd file.

    """
    header = {}
    data = {}
    comments = []

    skip = 0
    with open(filename, 'rb') as pcd:
        
        for line in pcd:
            if b"#" in line:
                comments.append(line.decode())
            if b"VERSION" in line:
                header["version"] = line.decode().split()[1]
            elif b"FIELDS" in line:
                header["fields"] = line.decode().split()[1:]
            elif b"SIZE" in line:
                header["size"] = line.decode().split()[1:]
            elif b"TYPE" in line:
                header["type"] = line.decode().split()[1:]
            elif b"COUNT" in line:
                header["count"] = line.decode().split()[1:]
            elif b"DATA" in line:
                header["data"] = line.decode().split()[1]
                skip+=1
                break
            skip +=1

        end_header = pcd.tell()
    
    data["comments"] = comments

    if "ascii" in header["data"]:
        data["points"] = pd.read_csv(filename, sep=" ", header=None, skiprows=skip,
                            names=header["fields"] )
        
        data["points"][["x", "y", "z"]] = data["points"][["x", "y", "z"]].astype("float32")
        # decode the WTFARETHAT rgb values from PCD
        rgb = data["points"]["rgb"].values.astype(int)
        data["points"]["red"] = np.asarray((rgb >> 16) & 255, dtype=np.uint8)
        data["points"]["green"]  = np.asarray((rgb >> 8) & 255, dtype=np.uint8)
        data["points"]["blue"] = np.asarray(rgb & 255, dtype=np.uint8)

        data["points"].drop("rgb", 1, inplace=True)

    else:
        raise NotImplementedError
    
    return data

def write_pcd(filename, points, comments=None):

    points = points.copy()
    
    if not filename.endswith('pcd'):
        filename += '.pcd'

    if set(['red', 'green', 'blue']).issubset(points.columns):
        # encode the WTFARETHAT rgb values for PCD
        rgb = points[["red", "green", "blue"]].values.astype(np.uint32)
        points.drop(["red", "green", "blue"], 1, inplace=True)
        points["rgb"] = np.array((rgb[:, 0] << 16) | (rgb[:, 1] << 8) | (rgb[:, 2] << 0),
                                    dtype=np.uint32)
        points = points[["x", "y", "z", "rgb"]]     
    else:
        points = points[["x", "y", "z"]]

    with open(filename, "w") as pcd:
        
        for line in comments:
            pcd.write("#%s\n" % line.strip())
        
        pcd.write("VERSION .7\n")
        pcd.write("FIELDS {}\n".format(" ".join(points.columns)))
        pcd.write("TYPE {}\n".format(" ".join([str(x)[0].upper() for x in points.dtypes])))
        pcd.write("COUNT {}\n".format(" ".join(["1"]*len(points.columns))))
        pcd.write("WIDTH {}\n".format(str(len(points))))
        pcd.write("HEIGHT 1\n")
        pcd.write("VIEWPOINT 0 0 0 1 0 0 0\n")
        pcd.write("POINTS {}\n".format(str(len(points))))
        pcd.write("DATA ascii\n")  

    points.to_csv(filename, sep=" ", index=False, header=False, mode='a',
                                                                encoding='ascii')     
