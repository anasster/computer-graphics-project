import numpy as np
from sort_points import *


def calculate_effective_points(vertices):
    # Function that calculates the effective points of a triangle
    
    # Sort the vertices of the triangle, so that y[0] = ymin and y[2] = ymax
    vertices = sort_points(vertices)
    ymin = np.min(vertices[:, 1])
    ymax = np.max(vertices[:, 1])
    xmin = np.min(vertices[:, 0])
    xmax = np.max(vertices[:, 0])
    yt = vertices[:, 1]
    xt = vertices[:, 0]
    # Create an empty list to save the effective points' x coordinate for each value of y.
    # The size of the list will be N x 2
    effectivePoints = []

    for y in range(ymin, ymax + 1):
        # Check for horizontal top side when y = ymin
        if y == ymin:
            if yt[0] == yt[1] == ymin:
                effectivePoints.append([xt[0], xt[1]])
            else:
                continue
            # Check for horizontal bottom side when y = ymax
        if y == ymax:
            if yt[1] == yt[2] == ymax:
                effectivePoints.append([xt[1], xt[2]])
            else:
                continue
            # While y scans the inside of the triangle, check for 3 different triangle forms:
        if ymin < y < ymax:
            # Form 1: No horizontal sides
            if yt[0] < yt[1] < yt[2]:
                if yt[0] < y <= yt[1]:
                    m1 = (xt[1] - xt[0]) / (yt[1] - yt[0])
                    m2 = (xt[2] - xt[0]) / (yt[2] - yt[0])
                    x1 = xt[1] + (y - yt[1]) * m1
                    x2 = xt[2] + (y - yt[2]) * m2
                    effectivePoints.append([x1, x2])
                else:
                    m1 = (xt[2] - xt[1]) / (yt[2] - yt[1])
                    m2 = (xt[2] - xt[0]) / (yt[2] - yt[0])
                    x1 = xt[2] + (y - yt[2]) * m1
                    x2 = xt[2] + (y - yt[2]) * m2
                    effectivePoints.append([x1, x2])
            # Form 2: Horizontal top side
            elif yt[0] == yt[1] == ymin:
                m1 = (xt[2] - xt[0]) / (yt[2] - yt[0])
                m2 = (xt[2] - xt[1]) / (yt[2] - yt[1])
                x1 = xt[2] + (y - yt[2]) * m1
                x2 = xt[2] + (y - yt[2]) * m2
                effectivePoints.append([x1, x2])
            # Form 3: Horizontal bottom side
            elif yt[1] == yt[2] == ymax:
                m1 = (xt[1] - xt[0]) / (yt[1] - yt[0])
                m2 = (xt[2] - xt[0]) / (yt[2] - yt[0])
                x1 = xt[1] + (y - yt[1]) * m1
                x2 = xt[2] + (y - yt[2]) * m2
                effectivePoints.append([x1, x2])
            # Any other form means that the 3 points are colinear
            else:
                raise ValueError("This is a straight line, not a triangle!")
    return np.array(effectivePoints, dtype = 'uint64')

