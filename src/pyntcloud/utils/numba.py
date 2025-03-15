from numba import njit


@njit
def groupby_count(xyz, indices, out):
    for i in range(xyz.shape[0]):
        out[indices[i]] += 1
    return out


@njit
def groupby_sum(xyz, indices, N, out):
    for i in range(xyz.shape[0]):
        out[indices[i]] += xyz[i][N]
    return out


@njit
def groupby_max(xyz, indices, N, out):
    for i in range(xyz.shape[0]):
        if xyz[i][N] > out[indices[i]]:
            out[indices[i]] = xyz[i][N]
    return out
