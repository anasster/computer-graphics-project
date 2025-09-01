import numpy as np
from interpolate_vectors import *


def gourauds(canvas, vertices, vcolors):
    # At first, we calculate the intersection points of the scanline with the triangle, exactly as in flats.
    xt = [0 for i in range(3)]
    yt = [0 for i in range(3)]
    for i in range(3):
        xt[i] = vertices[i, 0]
        yt[i] = vertices[i, 1]

    ymin = min(yt)
    ymax = max(yt)
    xmin = min(xt)
    xmax = max(xt)

    yt = np.array(yt)
    xt = np.array(xt)
    yindexes = np.argsort(yt)
    yt.sort()
    for i in range(3):
        xt[i] = xt[yindexes[i]]
    if yt[0] == yt[1]:
        xt[0] = min(xt[0], xt[1])
        xt[1] = max(xt[0], xt[1])
    if yt[1] == yt[2]:
        xt[1] = min(xt[1], xt[2])
        xt[2] = max(xt[1], xt[2])
    # Return the sorted coordinates to the vertices matrix
    for i in range(len(vertices)):
        vertices[i, 0] = xt[i]
        vertices[i, 1] = yt[i]
    # Sort the colors to the correct points
    for i in range(len(vcolors)):
        vcolors[i] = vcolors[yindexes[i]]
    effectivepoints = []
    for y in range(ymin + 1, ymax):
        if yt[0] == yt[1]:
            effectivepoints.append([int(xt[0] + (y - yt[0]) * (xt[2] - xt[0]) / (yt[2] - yt[0])),
                                    int(xt[1] + (y - yt[1]) * (xt[2] - xt[1]) / (yt[2] - yt[1]))])
        elif yt[1] == yt[2]:
            effectivepoints.append([int(xt[0] + (y - yt[0]) * (xt[1] - xt[0]) / (yt[1] - yt[0])),
                                    int(xt[0] + (y - yt[0]) * (xt[2] - xt[0]) / (yt[2] - yt[0]))])
        else:
            if yt[0] <= y <= yt[1]:
                effectivepoints.append([int(xt[0] + (y - yt[0]) * (xt[1] - xt[0]) / (yt[1] - yt[0])),
                                        int(xt[0] + (y - yt[0]) * (xt[2] - xt[0]) / (yt[2] - yt[0]))])
            else:
                effectivepoints.append([int(xt[1] + (y - yt[1]) * (xt[2] - xt[1]) / (yt[2] - yt[1])),
                                        int(xt[0] + (y - yt[0]) * (xt[2] - xt[0]) / (yt[2] - yt[0]))])

    for y in range(ymin, ymax + 1):
        # Case where triangle has a horizontal top side
        if y == ymin:
            if yt[0] == yt[1]:
                continue
        # Case where triangle has a horizontal bottom side
        elif y == ymax:
            if yt[1] == yt[2]:
                for x in range(xt[1] + 1, xt[2]):
                    tcolors = interpolate_vectors(vertices[1], vertices[2], vcolors[1], vcolors[2], x, 1)
                    canvas[y, x] = tcolors
        # Case where y scans between ymin and ymax
        else:
            Y = y - ymin - 1
            p1 = [min(effectivepoints[Y]), y]
            p2 = [max(effectivepoints[Y]), y]
            # Examine if top side is horizontal
            if yt[0] == yt[1]:
                canvas[y, p1[0]] = interpolate_vectors(vertices[0], vertices[2], vcolors[0], vcolors[2], y, 2)
                canvas[y, p2[0]] = interpolate_vectors(vertices[1], vertices[2], vcolors[1], vcolors[2], y, 2)
                for x in range(p1[0] + 1, p2[0]):
                    canvas[y, x] = interpolate_vectors(p1, p2, canvas[y, p1[0]], canvas[y, p2[0]], x, 1)
            # Examine if bottom side is horizontal
            elif yt[1] == yt[2]:
                canvas[y, p1[0]] = interpolate_vectors(vertices[0], vertices[1], vcolors[0], vcolors[1], y, 2)
                canvas[y, p2[0]] = interpolate_vectors(vertices[0], vertices[2], vcolors[0], vcolors[2], y, 2)
                for x in range(p1[0] + 1, p2[0]):
                    canvas[y, x] = interpolate_vectors(p1, p2, canvas[y, p1[0]], canvas[y, p2[0]], x, 1)
            # Case where no side is horizontal
            else:
                if y <= yt[1]:
                    canvas[y, p1[0]] = interpolate_vectors(vertices[0], vertices[1], vcolors[0], vcolors[1], y, 2)
                    canvas[y, p2[0]] = interpolate_vectors(vertices[0], vertices[2], vcolors[0], vcolors[2], y, 2)
                    for x in range(p1[0] + 1, p2[0]):
                        canvas[y, x] = interpolate_vectors(p1, p2, canvas[y, p1[0]], canvas[y, p2[0]], x, 1)
                else:
                    canvas[y, p1[0]] = interpolate_vectors(vertices[1], vertices[2], vcolors[1], vcolors[2], y, 2)
                    canvas[y, p2[0]] = interpolate_vectors(vertices[0], vertices[2], vcolors[0], vcolors[2], y, 2)
                    for x in range(p1[0] + 1, p2[0]):
                        canvas[y, x] = interpolate_vectors(p1, p2, canvas[y, p1[0]], canvas[y, p2[0]], x, 1)


    updatedcanvas = canvas
    return updatedcanvas
