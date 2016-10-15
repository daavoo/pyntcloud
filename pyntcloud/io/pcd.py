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
        data["vertex"] = pd.read_csv(filename, sep=" ", header=None, skiprows=skip,
                            names=header["fields"] )
        
        data["vertex"][["x", "y", "z"]] = data["vertex"][["x", "y", "z"]].astype("float32")
        # decode the WTFARETHAT rgb values from PCD
        rgb = data["vertex"]["rgb"].values.astype(int)
        data["vertex"]["red"] = np.asarray((rgb >> 16) & 255, dtype=np.uint8)
        data["vertex"]["green"]  = np.asarray((rgb >> 8) & 255, dtype=np.uint8)
        data["vertex"]["blue"] = np.asarray(rgb & 255, dtype=np.uint8)

        data["vertex"].drop("rgb", 1, inplace=True)

    else:
        raise NotImplementedError
    
    return data

def write_pcd(filename, vertex, comments=None):

    if not filename.endswith('pcd'):
        filename += '.pcd'

    if set(['red', 'green', 'blue']).issubset(vertex.columns):
        # encode the WTFARETHAT rgb values for PCD
        rgb = vertex[["red", "green", "blue"]].values.astype(np.uint32)
        vertex.drop(["red", "green", "blue"], 1, inplace=True)
        vertex["rgb"] = np.array((rgb[:, 0] << 16) | (rgb[:, 1] << 8) | (rgb[:, 2] << 0),
                                    dtype=np.uint32)
        vertex = vertex[["x", "y", "z", "rgb"]]     
    else:
        vertex = vertex[["x", "y", "z"]]

    with open(filename, "w") as pcd:
        
        for line in comments:
            pcd.write("#%s\n" % line.strip())
        
        pcd.write("VERSION .7\n")
        pcd.write("FIELDS {}\n".format(" ".join(vertex.columns)))
        pcd.write("TYPE {}\n".format(" ".join([str(x)[0].upper() for x in vertex.dtypes])))
        pcd.write("COUNT {}\n".format(" ".join(["1"]*len(vertex.columns))))
        pcd.write("WIDTH {}\n".format(str(len(vertex))))
        pcd.write("HEIGHT 1\n")
        pcd.write("VIEWPOINT 0 0 0 1 0 0 0\n")
        pcd.write("POINTS {}\n".format(str(len(vertex))))
        pcd.write("DATA ascii\n")  

    vertex.to_csv(filename, sep=" ", index=False, header=False, mode='a',
                                                                encoding='ascii')     
