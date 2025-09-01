import numpy as np


def inside_panel(verts, M, N):
    xmin, xmax = 0, N
    ymin, ymax = 0, M
    inside = True
    for x in verts[0, :]:
        if x < 0 or x > N - 1:
            inside = False
    for y in verts[1, :]:
        if y < 0 or y > M - 1:
            inside = False
    return inside