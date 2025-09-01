import numpy as np


def change_coordinate_system(cp, R, c0):
    # Function that changes a point's coordinate system by rotating and moving the axes
    N = cp.shape[1] if len(cp.shape) > 1 else 1
    dp = np.empty((3, N))
    for i in range(N):
        # Since rotating/translating the axes is the inverse procedure of rotating translating the points,
        # and R is an SO3 matrix (RT = R^-1), the formula instructs:
        if N > 1:
            dp[:, i] = np.transpose(R).dot(cp[:, i] - c0)
        else:
            dp = np.transpose(R).dot(cp - c0) 
    return dp