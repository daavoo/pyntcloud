#       HAKUNA MATATA

# Contributed by: Nicholas Mitchell

import numpy as np
import pandas as pd


def read_bin(filename, shape=None, **kwargs):
    """ Read a _raw binary_ file and store all possible elements in pandas DataFrame.

    If the shape of the array is known, it can be specified using
    `shape`. The first three columns are used for x, y and z.
    Otherwise the binary file is assumed have row-major format and
    three columns are formed.

    NOTE: binary files that are not `raw` will not behave as expected. If they
    contain a header/footer with meta data, or were generated e.g. via Protobuf,
    then bahviour is also undefined.

    Parameters
    ----------
    filename: str
        Path to the filename
    shape: shape of array if known, optional.
    **kwargs:
    kwargs: numpy.fromfile supported kwargs
        Check NumPy documentation for all possibilities.

    Returns
    -------
    data: dict
        If possible, elements as pandas DataFrames else a NumPy ndarray
    """
    data = {}

    kwargs['dtype'] = kwargs.get('dtype', np.float32)
    arr = np.fromfile(filename, **kwargs)
    n_elements = arr.size

    if shape is not None:
        try:
            arr = arr.reshape(shape)
        except ValueError:
            raise ValueError(('The array cannot be reshaped to {0} as '
                              'it has {1} elements, which is not '
                              'divisible by three'.format(shape, n_elements)))
    else:
        arr = arr.reshape((-1, 3))
        pass

    data["points"] = pd.DataFrame(arr[:, 0:3], columns=['x', 'y', 'z'])

    return data


def write_bin(filename, **kwargs):
    """Write the raw point data in `PyntCloud.xyz` to a binary file.

    Parameters
    ----------
    filename: str
        The created file will be named with this
    kwargs: numpy.ndarray.tofile supported kwargs
        Check NumPy documentation on raw binary files for all possibilities.

    Returns
    -------
    boolean
        True if no problems
    """
    if kwargs['also_save'] is not None:
        raise ValueError(('Can only write the PyntCloud.xyz array. '
                          'Please remove argument `also_save`'))
    else:
        # Remove so it does not get passed to nd.array.tofile()
        del kwargs['also_save']
        np.ndarray.tofile(filename, **kwargs)

    return True
