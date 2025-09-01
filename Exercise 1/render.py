import numpy as np
from flats import *
from gourauds import *


def render(verts2d, faces, vcolors, depth, shade_t):
    k = len(faces)  # Total number of triangles
    l = len(depth)  # Total number of vertices
    canvas = np.ones((512, 512, 3))
    img = np.empty((512, 512, 3))

    # List with the depth of each triangle
    tdepth = np.zeros(k)

    for i in range(k):
        for j in range(3):
            tdepth[i] += depth[faces[i, j]]

    # The depth of each triangle is the mean of its vertices depth
    for i in range(len(tdepth)):
        tdepth[i] /= 3

    # Create a list containing the coordinates of the triangle to be colored
    tcolored = np.zeros((3, 2))
    colors = np.zeros((3, 3))
    depth_indexes = np.argsort(-tdepth)
    for i in range(k):
        tcolored = verts2d[faces[depth_indexes[i]]]
        colors = vcolors[faces[depth_indexes[i]]]
        for j in range(3):
            canvas[tcolored[j, 1], tcolored[j, 0]] = colors[j]
        if shade_t == 'flat':
            img = flats(canvas, tcolored, colors)
        elif shade_t == 'gouraud':
            img = gourauds(canvas, tcolored, colors)
        else:
            raise ValueError("Choose a valid coloring method")

    return img
