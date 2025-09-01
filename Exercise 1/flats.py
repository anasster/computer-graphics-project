import numpy as np


def flats(canvas, vertices, vcolors):
    xt = [0 for i in range(3)]
    yt = [0 for i in range(3)]
    for i in range(3):
        xt[i] = vertices[i][0]  # x coordinate of each triangle's vertex
        yt[i] = vertices[i][1]  # y coordinate of each triangle's vertex
    # Calculate boundaries of scanning box
    ymin = min(yt)
    ymax = max(yt)
    xmin = min(xt)
    xmax = max(xt)

    # Sort the coordinates' indexes in increasing order of y
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
    # Sort the colors to the correct points
    for i in range(len(vcolors)):
        vcolors[i] = vcolors[yindexes[i]]
    # Create an empty list to save the triangle's effective points. They will be saved in an K by 2 list, where each
    # row contains the two intersection points of the scanline with the triangle's sides. We can be certain that the
    # scanline intercepts with exactly 2 points, as the triangle is a convex polygon. Note that this list saves the
    # effective points while y is not ymin or ymax, as those special cases are examined alone.

    effectivepoints = []
    for y in range(ymin + 1, ymax):
        # Case where top side is horizontal
        if yt[0] == yt[1]:
            effectivepoints.append([int(xt[0] + (y - yt[0]) * (xt[2] - xt[0]) / (yt[2] - yt[0])),
                                    int(xt[1] + (y - yt[1]) * (xt[2] - xt[1]) / (yt[2] - yt[1]))])
        # Case where bottom side is horizontal
        elif yt[1] == yt[2]:
            effectivepoints.append([int(xt[0] + (y - yt[0]) * (xt[1] - xt[0]) / (yt[1] - yt[0])),
                                    int(xt[0] + (y - yt[0]) * (xt[2] - xt[0]) / (yt[2] - yt[0]))])
        # Case where there are no horizontal sides
        else:
            if yt[0] <= y <= yt[1]:
                effectivepoints.append([int(xt[0] + (y - yt[0]) * (xt[1] - xt[0]) / (yt[1] - yt[0])),
                                        int(xt[0] + (y - yt[0]) * (xt[2] - xt[0]) / (yt[2] - yt[0]))])
            else:
                effectivepoints.append([int(xt[1] + (y - yt[1]) * (xt[2] - xt[1]) / (yt[2] - yt[1])),
                                        int(xt[0] + (y - yt[0]) * (xt[2] - xt[0]) / (yt[2] - yt[0]))])

    # RGB vector for points inside the triangle
    tcolors = [0 for i in range(3)]
    for i in range(3):
        tcolors[0] += vcolors[i][0]  # R as a mean of the vertices' R
        tcolors[1] += vcolors[i][1]  # G as a mean of the vertices' G
        tcolors[2] += vcolors[i][2]  # B as a mean of the vertices' B

    # The RGB value of each point is the mean of the vertices' RGB
    for i in range(3):
        tcolors[i] /= 3
    tcolors = np.array(tcolors)

    # Coloring the triangle
    
    for y in range(ymin, ymax + 1):
        # At ymin, we check for a horizontal side
        if y == ymin:
            if yt[0] == yt[1]:
                continue
        # At ymax, we check for a horizontal side
        elif y == ymax:
            if yt[1] == yt[2]:
                for x in range(xt[1], xt[2] + 1):
                    canvas[y, x] = tcolors
        # The rest of the triangle is colored regardless of whether a horizontal side exists
        else:
            Y = y - ymin - 1
            x1 = min(effectivepoints[Y])
            x2 = max(effectivepoints[Y])
            for x in range(x1, x2 + 1):
                canvas[y, x] = tcolors

    updatedcanvas = canvas
    return updatedcanvas
