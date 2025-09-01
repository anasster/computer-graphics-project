import numpy as np
from gourauds import *


def render(verts2d, faces, vcolors, depth):
    k = len(faces)  # Total number of triangles
    l = len(depth)  # Total number of vertices
    canvas = np.ones((512, 512, 3))
    img = np.empty((512, 512, 3))

    # List with the depth of each triangle's vertex
    vdepths = np.empty((k, 3))
    vdepths[:, :] = depth[faces[:, :]]
           
    # The depth of each triangle is the mean of its vertices depth
    tdepth = np.empty(k)
    tdepth = np.mean(depth[faces], axis=1)

    # Create a list containing the coordinates of the triangle to be colored
    tcolored = np.zeros((3, 2))
    colors = np.zeros((3, 3))
    depth_indexes = np.argsort(-tdepth)
    for i in range(k):
        for j in range(3):
            tcolored[j, :] = verts2d[faces[depth_indexes[i], j], :]
            colors[j, :] = vcolors[faces[depth_indexes[i], j], :]
            canvas[np.int64(tcolored[j, 1]), np.int64(tcolored[j, 0]), :] = colors[j, :]
        img = gourauds(canvas, tcolored, colors)
    return img
