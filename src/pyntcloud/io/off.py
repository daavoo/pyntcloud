import pandas as pd
import numpy as np


def read_off(filename):
    with open(filename) as off:
        first_line = off.readline()
        if "OFF" not in first_line:
            raise ValueError("The file does not start with the word OFF")
        color = True if "C" in first_line else False

        n_points = 0
        n_faces = 0

        count = 1
        for line in off:
            count += 1
            if line.startswith("#"):
                continue
            line = line.strip().split()
            if len(line) > 1:
                n_points = int(line[0])
                n_faces = int(line[1])
                break

        if n_points == 0:
            raise ValueError("The file has no points")

        data = {}
        point_names = ["x", "y", "z"]
        point_types = {"x": np.float32, "y": np.float32, "z": np.float32}

        if color:
            point_names.extend(["red", "green", "blue"])
            point_types = dict(
                point_types, **{"red": np.uint8, "green": np.uint8, "blue": np.uint8}
            )

        data["points"] = pd.read_csv(
            off,
            sep=" ",
            header=None,
            engine="c",
            nrows=n_points,
            names=point_names,
            dtype=point_types,
            index_col=False,
            comment="#",
        )

        data["mesh"] = pd.read_csv(
            filename,
            sep=" ",
            header=None,
            engine="c",
            skiprows=(count + n_points),
            nrows=n_faces,
            usecols=[1, 2, 3],
            names=["v1", "v2", "v3"],
            comment="#",
        )
        return data
