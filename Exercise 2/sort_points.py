import numpy as np


def sort_points(points):
    # Function that sorts the vertices of a triangle, first by increasing order of y and then 
    # by increasing order of x, if need be.
    x = points[:, 0]
    y = points[:, 1]
    y_indices = np.argsort(y)
    y = y[y_indices]
    x = x[y_indices]
    for i in range(1, len(y)):
        # In case of equal y coordinates, sort by increasing x coordinates
        if y[i] == y[i - 1]:
            if x[i] < x[i - 1]:
                x[i], x[i - 1] = x[i - 1], x[i]
    
    sorted_points = np.empty((len(y), 2), dtype='int64')
    sorted_points[:, 0] = x
    sorted_points[:, 1] = y
    return sorted_points
