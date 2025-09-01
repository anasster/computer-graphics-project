import numpy as np
from interpolate_vectors import *
from sort_points import *
from calculate_effective_points import *


def gourauds(canvas, vertices, vcolors):
    vcolors = vcolors[np.argsort(vertices[:, 1])]
    vertices = sort_points(vertices)
    xt = vertices[:, 0] # x coordinate of each triangle's vertex
    yt = vertices[:, 1] # y coordinate of each triangle's vertex
    # Calculate boundaries of scanning box
    ymin = np.min(yt)
    ymax = np.max(yt)
    xmin = np.min(xt)
    xmax = np.max(xt)

    # Calculate the effective points of the triangle
    effectivePoints = calculate_effective_points(vertices)

    # Begin shading the triangle, checking for 3 possible triangle forms
    if yt[0] == yt[1] == ymin:
        for y in range(ymin, ymax):
            Y = y - ymin
            x1 = int(np.min(effectivePoints[Y]))
            x2 = int(np.max(effectivePoints[Y]))
            p1 = np.array([x1, y])
            p2 = np.array([x2, y])
            canvas[y, x1] = interpolate_vectors(vertices[0], vertices[2], vcolors[0], vcolors[2], y, 2)
            canvas[y, x2] = interpolate_vectors(vertices[1], vertices[2], vcolors[1], vcolors[2], y, 2)
            for x in range(x1 + 1, x2):
                canvas[y, x] = interpolate_vectors(p1, p2, canvas[y, x1], canvas[y, x2], x, 1)
    elif yt[1] == yt[2] == ymax:
        for y in range(ymin + 1, ymax + 1):
            Y = y - ymin - 1
            x1 = int(np.min(effectivePoints[Y]))
            x2 = int(np.max(effectivePoints[Y]))
            p1 = np.array([x1, y])
            p2 = np.array([x2, y])
            canvas[y, x1] = interpolate_vectors(vertices[0], vertices[1], vcolors[0], vcolors[1], y, 2)
            canvas[y, x2] = interpolate_vectors(vertices[0], vertices[2], vcolors[0], vcolors[2], y, 2)
            for x in range(x1 + 1, x2):
                canvas[y, x] = interpolate_vectors(p1, p2, canvas[y, x1], canvas[y, x2], x, 1)
    elif yt[0] < yt[1] < yt[2]:
        for y in range(ymin + 1, ymax):
            Y = y - ymin - 1
            x1 = int(np.min(effectivePoints[Y]))
            x2 = int(np.max(effectivePoints[Y]))
            p1 = np.array([x1, y])
            p2 = np.array([x2, y])
            if yt[0] < y <= yt[1]:
                canvas[y, x1] = interpolate_vectors(vertices[0], vertices[1], vcolors[0], vcolors[1], y, 2)
                canvas[y, x2] = interpolate_vectors(vertices[0], vertices[2], vcolors[0], vcolors[2], y, 2)
                for x in range(x1 + 1, x2):
                    canvas[y, x] = interpolate_vectors(p1, p2, canvas[y, x1], canvas[y, x2], x, 1)
            else:
                canvas[y, x1] = interpolate_vectors(vertices[1], vertices[2], vcolors[1], vcolors[2], y, 2)
                canvas[y, x2] = interpolate_vectors(vertices[0], vertices[2], vcolors[0], vcolors[2], y, 2)
                for x in range(x1 + 1, x2):
                    canvas[y, x] = interpolate_vectors(p1, p2, canvas[y, x1], canvas[y, x2], x, 1)

    updatedcanvas = canvas
    return updatedcanvas
