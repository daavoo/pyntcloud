import pandas as pd


def read_off(filename):

    with open(filename) as off:

        if "OFF" not in off.readline():
            raise ValueError('The file does not start whith the word OFF')

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

        data = {}

        data["points"] = pd.read_csv(filename, sep=" ", header=None, engine="python",
                                     skiprows=count, skip_footer=n_faces,
                                     names=["x", "y", "z"])

        data["mesh"] = pd.read_csv(filename, sep=" ", header=None, engine="python",
                                   skiprows=(count + n_points), usecols=[1, 2, 3],
                                   names=["v1", "v2", "v3"])
        return data
