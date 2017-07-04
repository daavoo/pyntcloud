import numpy as np
from scipy.ndimage import affine_transform


def apply_offset(matrix, x, y, z):
    """ Needed in order to rotate along center of the voxelgrid.

    Parameters
    ----------
    matrix : (4,4) ndarray
    x, y, z : uint
        Dimensions of the voxelgrid.
    """
    o_x = float(x) / 2 + 0.5
    o_y = float(y) / 2 + 0.5
    o_z = float(z) / 2 + 0.5

    offset_matrix = np.array([[1, 0, 0, o_x],
                              [0, 1, 0, o_y],
                              [0, 0, 1, o_z],
                              [0, 0, 0, 1]])

    reset_matrix = np.array([[1, 0, 0, -o_x],
                             [0, 1, 0, -o_y],
                             [0, 0, 1, -o_z],
                             [0, 0, 0, 1]])

    transform_matrix = np.dot(np.dot(offset_matrix, matrix), reset_matrix)

    return transform_matrix


def apply_transform(x, transform_matrix, channel_axis, fill_mode="constant", cval=0.):
    x = np.rollaxis(x, channel_axis, 0)
    final_affine_matrix = transform_matrix[:3, :3]
    final_offset = transform_matrix[:3, 3]
    channel_images = [affine_transform(x_channel,
                                       final_affine_matrix,
                                       final_offset,
                                       order=0,
                                       mode=fill_mode,
                                       cval=cval) for x_channel in x]
    x = np.stack(channel_images, axis=0)
    x = np.rollaxis(x, 0, channel_axis + 1)
    return x


def combine_transforms(transforms):
    """ Merge affine transforms into 1 single matrix
    """
    t = transforms[0]
    for i in range(1, len(transforms)):
        t = np.dot(t, transforms[i])
    return t


def Rx(angle, degrees=True):
    if degrees:
        cx = np.cos(np.deg2rad(angle))
        sx = np.sin(np.deg2rad(angle))
    else:
        cx = np.cos(angle)
        sx = np.sin(angle)
    return np.array([[1, 0, 0, 0],
                     [0, cx, sx, 0],
                     [0, -sx, cx, 0],
                     [0, 0, 0, 1]])


def Ry(angle, degrees=True):
    if degrees:
        cy = np.cos(np.deg2rad(angle))
        sy = np.sin(np.deg2rad(angle))
    else:
        cy = np.cos(angle)
        sy = np.sin(angle)
    return np.array([[cy, 0, -sy, 0],
                     [0, 1, 0, 0],
                     [sy, 0, cy, 0],
                     [0, 0, 0, 1]])


def Rz(angle, degrees=True):
    if degrees:
        cz = np.cos(np.deg2rad(angle))
        sz = np.sin(np.deg2rad(angle))
    else:
        cz = np.cos(angle)
        sz = np.sin(angle)
    return np.array([[cz, sz, 0, 0],
                     [-sz, cz, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def shift_voxels(tx, ty, tz):
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])


def flip_axis(x, axis):
    x = np.asarray(x).swapaxes(axis, 0)
    x = x[::-1, ...]
    x = x.swapaxes(0, axis)
    return x


def random_channel_shift(x, intensity, channel_axis=0):
    x = np.rollaxis(x, channel_axis, 0)
    min_x, max_x = np.min(x), np.max(x)
    channel_images = [np.clip(x_channel + np.random.uniform(-intensity, intensity), min_x, max_x)
                      for x_channel in x]
    x = np.stack(channel_images, axis=0)
    x = np.rollaxis(x, 0, channel_axis + 1)
    return x
