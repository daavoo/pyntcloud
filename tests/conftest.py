import pytest

import numpy as np
import pandas as pd

from pyntcloud import PyntCloud


@pytest.fixture()
def xyz():
    return np.array([
        [0. , 0. , 0. ],
        [0.1, 0.1, 0.1],
        [0.2, 0.2, 0.2],
        [0.5, 0.5, 0.5],
        [0.9, 0.9, 0.9],
        [1. , 1. , 1. ]], dtype=np.float32)


@pytest.fixture()
@pytest.mark.usefixtures("xyz")
def simple_pyntcloud(xyz):
    return PyntCloud(pd.DataFrame(
        data=xyz,
        columns=["x", "y", "z"]))


@pytest.fixture()
@pytest.mark.usefixtures("simple_pyntcloud")
def pyntcloud_with_kdtree(simple_pyntcloud):
    simple_pyntcloud.add_structure("kdtree")
    return simple_pyntcloud

