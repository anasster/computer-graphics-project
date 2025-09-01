import numpy as np
from change_coordinate_system import *


def pinhole(f, cv, cx, cy, cz, p3d):
    # Function that performs perspective projection to N 3D points, using a pinhole camera
    # According to theory, the WCS coordinates of the camera unitary vectors, form a rotation matrix
    # which we use to find the coordinates of a point P in the CCS
    R = [cx, cy, cz]
    N = len(p3d)
    p3dc = change_coordinate_system(p3d, R, cv)
    # Now that we know the coordinates of P in the CCS, we perform the projection
    p2d = np.empty((N, 2))
    depth = np.empty(N)
    for i in range(N):
        p2d[i, 0] = f * p3dc[i, 0] / p3dc[i, 2]
        p2d[i, 1] = f * p3dc[i, 1] / p3dc[i, 2] 
        depth[i] = p3dc[i, 2]
    return p2d, depth