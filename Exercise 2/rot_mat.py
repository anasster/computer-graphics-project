import numpy as np


def rot_mat(theta, u):
    # Function that calculates the rotation matrix of a counter-clockwise rotation by theta rads around an axis parallel to the vector u
    # Normalize the vector u
    u = u / np.linalg.norm(u)
    ux = u[0]
    uy = u[1]
    uz = u[2]
    c = np.cos(theta)
    s = np.sin(theta)
    # Calculate R using Rodriguez's formula

    R = np.array([[(1-c)*ux**2+c, (1-c)*ux*uy-s*uz, (1-c)*ux*uz+s*uy],
                  [(1-c)*uy*ux+s*uz, (1-c)*uy**2+c, (1-c)*uy*uz-s*ux],
                  [(1-c)*uz*ux-s*uy, (1-c)*uz*uy+s*ux, (1-c)*uz**2+c]])
    return R
