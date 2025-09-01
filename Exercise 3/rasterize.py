import numpy as np


def rasterize(p2d, rows, cols, h, w):
    # Function that takes K 2D points projected to the (h x w) panel of a camera, and transforms their real coordinates into 
    # integer coordinates on a (rows x cols) sized raster
    K = p2d.shape[1]
    n2d = np.empty((2, K))
    for i in range(K):
        n2d[:, i] = np.round(np.array([cols / 2, rows / 2]) + np.array([p2d[0, i] * cols / w, p2d[1, i] * rows / h]))
    return n2d
