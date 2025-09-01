import numpy as np


def interpolate_vectors(p1, p2, v1, v2, xy, dim):
    v = np.empty((len(v1),))
    if dim == 1:
        # Interpolate in x dimension
        t = np.abs((xy - p1[0]) / (p2[0] - p1[0])) if p1[0] != p2[0] else 1
    elif dim == 2:
        # Interpolate in y dimension
        t = np.abs((xy - p1[1]) / (p2[1] - p1[1])) if p1[1] != p2[1] else 1

    else:
        raise ValueError("Dim can only take values 1 or 2!!!")
    l = len(v1)
    if len(v1) == len(v2):
        for i in range(l):
            v[i] = np.abs(t * v1[i] + (1 - t) * v2[i])
    else:
        raise TypeError("Vectors v1 and v2 must have the same dimensions")
    return v
