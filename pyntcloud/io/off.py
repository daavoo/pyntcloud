import re

import numpy as np
import pandas as pd


def read_off(filename):
    with open(filename) as f:
        first_line = f.readline()
        if "OFF" not in first_line:
            raise ValueError("The file does not start with the word OFF")
        has_color = "C" in first_line

        num_rows = None
        n_points = None
        n_faces = None
        n_header = 1

        # Backtrack to account for faulty headers, e.g. "OFF4 4 0".
        m = re.match(r"^(?P<prefix>\D+)([\d\s]+)$", first_line)
        if m:
            f.seek(len(m.group("prefix")))
            n_header = 0

        # Read header.
        for line in f:
            n_header += 1
            if line.startswith("#"):
                continue
            line = line.strip().split()
            if len(line) <= 1:
                continue
            n_points = int(line[0])
            n_faces = int(line[1])
            num_rows = n_points + n_faces
            break

        if num_rows is None:
            raise ValueError("The file does not contain a valid header")

        if n_points == 0:
            raise ValueError("The file contains no points")

        data = {}
        point_names = ["x", "y", "z"]
        point_types = {"x": np.float32, "y": np.float32, "z": np.float32}

        if has_color:
            point_names.extend(["red", "green", "blue"])
            color_point_types = {"red": np.uint8, "green": np.uint8, "blue": np.uint8}
            point_types = {**point_types, **color_point_types}

        data["points"] = pd.read_csv(
            f,
            sep=" ",
            header=None,
            engine="c",
            nrows=n_points,
            names=point_names,
            dtype=point_types,
            index_col=False,
            comment="#",
        )

        assert len(data["points"]) == n_points

        f.seek(0)

        data["mesh"] = pd.read_csv(
            f,
            sep=" ",
            header=None,
            engine="c",
            skiprows=n_header + n_points,
            nrows=n_faces,
            usecols=[1, 2, 3],
            names=["v1", "v2", "v3"],
            comment="#",
        )

        assert len(data["mesh"]) == n_faces

    return data
