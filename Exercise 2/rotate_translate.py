import numpy as np
from rot_mat import *


def rotate_translate(cp, theta, u, A, t):
    # Function that rotates a set of 3D points around an axis parallel to the vector u crossing the point A, and then moves them by t, where t a vector

    # Normalize u
    u = u/np.linalg.norm(u)
    # At first, we center the coordinate system to the point A. Hence, the rotation axis parallel to u will be crossing the center of the
    # new coordinate system
    d = np.array(A)
    # From now on, we work for N 3D points
    N = len(cp)
    cp_rot = np.empty((N, 3))
    cq =  np.empty((N, 3))
    R = rot_mat(theta, u)
    for i in range(N):
        # Switch coordinate system
        cp[i] = cp[i] - d
        # Rotate cp around the axis
        cp_rot[i] = R.dot(cp[i])
        # Bring rotated cp back to the original coordinate system
        cp_rot[i] = cp_rot[i] + d
        # Perform affine transform
        cq[i] = cp_rot[i] + t
    return cq
