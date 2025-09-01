import numpy as np
from pinhole import *


def camera_looking_at(f, cv, ck, cup, p3d):
    # Function that performs perspective projection of N 3D points by
    # using the vector of the target point, the camera center and the 
    # up vector.
    # At first we calculate the camera unitary vectors' coordinates
    # Unitary z
    z = ck - cv
    # Normalize
    cz = z / np.linalg.norm(z)

    # Unitary y
    t = cup - np.dot(cup, cz) * cz
    # Normalize
    cy = t / np.linalg.norm(t)

    # Unitary x
    x = np.cross(cy, cz)
    # Normalize
    cx = x / np.linalg.norm(x)

    p2d, depth = pinhole(f, cv, cx, cy, cz, p3d)
    return p2d, depth
    