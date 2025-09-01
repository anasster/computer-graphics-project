import numpy as np
from change_coordinate_system import *


def pinhole(f, cv, cx, cy, cz, p3d):
    # Function that performs perspective projection to N 3D points, using a pinhole camera
    # According to theory, the WCS coordinates of the camera unitary vectors, form a rotation matrix
    # which we use to find the coordinates of a point P in the CCS
    R = np.column_stack((cx, cy, cz))
    N = p3d.shape[1]
    p3dc = change_coordinate_system(p3d, R, cv)
    # Now that we know the coordinates of P in the CCS, we perform the projection
    p2d = np.empty((2, N))
    depth = np.empty(N)
    for i in range(N):
        p2d[0, i] = f * p3dc[0, i] / p3dc[2, i]
        p2d[1, i] = f * p3dc[1, i] / p3dc[2, i] 
        depth[i] = p3dc[2, i]
    return p2d, depth