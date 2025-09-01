import numpy as np


def rasterize(p2d, rows, cols, h, w):
    # Function that takes K 2D points projected to the (h x w) panel of a camera, and transforms their real coordinates into 
    # integer coordinates on a (rows x cols) sized raster
    K = len(p2d)
    n2d = np.empty((K, 2))
    for i in range(K):
        n2d[i] = np.uint16(np.array([cols / 2, rows / 2]) + np.array([p2d[i, 0] * cols / w, -p2d[i, 1] * rows / h]))
    return n2d
