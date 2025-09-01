import numpy as np
from gourauds import *
from render import *
from camera_looking_at import *
from rasterize import *


def render_object(p3d, faces, vcolors, h, w, rows, cols, f, cv, ck, cup):
    # Function that depicts an object on the camera panel through perspective projection, creates a raster
    # making the coordinates of the object's triangles integer, and finally rendering it by the gouraud method
    p2d, depth = camera_looking_at(f, cv, ck, cup, p3d)
    n2d = rasterize(p2d, rows, cols, h, w)
    img = render(n2d, faces, vcolors, depth)
    return img
