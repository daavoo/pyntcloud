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
            print(line)
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
        print (skip)
        
        end_header = pcd.tell()
    
    data["comments"] = comments

    if "ascii" in header["data"]:
        data["vertex"] = pd.read_csv(filename, sep=" ", header=None, skiprows=skip,
                            names=header["fields"] )
        
        # decode the WTFARETHAT rgb values from PCD
        rgb = data["vertex"]["rgb"].values.astype(int)
        data["vertex"]["r"] = np.asarray((rgb >> 16) & 255, dtype=np.uint8)
        data["vertex"]["g"]  = np.asarray((rgb >> 8) & 255, dtype=np.uint8)
        data["vertex"]["b"] = np.asarray(rgb & 255, dtype=np.uint8)

        data["vertex"].drop("rgb", 1, inplace=True)

    else:
        raise NotImplementedError
    
    return data

def write_pcd(filename, vertex):

    if not filename.endswith('pcd'):
    filename += '.pcd'

    with open(filename, "w") as obj:
        pass
