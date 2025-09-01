import numpy as np


def change_coordinate_system(cp, R, c0):
    # Function that changes a point's coordinate system by rotating and moving the axes
    N = len(cp)
    dp = np.empty((N, 3))
    for i in range(N):
        # Since rotating/translating the axes is the inverse procedure of rotating translating the points,
        # and R is an SO3 matrix (RT = R^-1), the formula instructs:
        dp[i] = np.transpose(R).dot(cp[i] - c0)
    return dp