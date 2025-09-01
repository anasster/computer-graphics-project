import numpy as np
from phong_material import *
from point_light import *
from camera_looking_at import *
from rasterize import *
from light import *
from calculate_normals import *
from inside_panel import *
from change_coordinate_system import *
from shade_gouraud import *
from shade_phong import *


def render_object(shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors, faces, mat, lights, light_amb):
    k = faces.shape[1]  # Total number of triangles
    l = verts.shape[1]  # Total number of vertices
    p2d, depth = camera_looking_at(focal, eye, lookat, up, verts)
    normals = calculate_normals(verts, faces)
    verts2d = rasterize(p2d, M, N, H, W)
    
    for i in range(k):
        if not inside_panel(verts2d[:, faces[:, i]], M, N):
            verts2d[:, faces] = np.delete(verts2d[:, faces], faces[:, i])
            depth[faces] = np.delete(depth[faces[:, i]], faces[:, i])
    
    canvas = np.empty((M, N, 3), dtype=float)
    canvas[:, :] = bg_color
    img = np.ones((M, N, 3)) * bg_color

    # List with the depth of each triangle's vertex
    vdepths = depth[faces]
           
    # The depth of each triangle is the mean of its vertices depth
    tdepth = np.mean(vdepths, axis=0)
    # Create a list containing the coordinates of the triangle to be colored
    tcolored = np.empty((2, 3))
    vcolors = np.empty((3, 3))
    norms = np.empty((3, 3))
    depth_indexes = np.argsort(tdepth)[::-1] # Sort the triangles' depths in decreasing order
    faces = faces[:, depth_indexes]
    for i in range(k):
        bcoords = np.mean(verts[:, faces[:, i]], axis=1)
        for j in range(3):
            tcolored[:, j] = verts2d[:, faces[j, i]]
            vcolors[:, j] = vert_colors[:, faces[j, i]]
            norms[:, j] = normals[:, faces[j, i]]
        if shader == 'gouraud':
            img = shade_gouraud(tcolored, norms, vcolors, bcoords, eye, mat, lights, light_amb, canvas)
        elif shader == 'phong':
            img = shade_phong(tcolored, norms, vcolors, bcoords, eye, mat, lights, light_amb, canvas)
        else:
            raise ValueError('Shader can only be \'gouraud\' or \'phong\'')

    return img