import numpy as np
import matplotlib.pyplot as plt
from point_light import PointLight
from phong_material import PhongMaterial
from render_object import *


data = np.load('h3.npy', allow_pickle=True, encoding='ASCII').item()
verts = data['verts']
vcolors = data['vertex_colors']
faces = data['face_indices']
cam_eye = data['cam_eye']
cam_lookat = data['cam_lookat']
cam_up = data['cam_up']
ka = data['ka']
kd = data['kd']
ks = data['ks']
n = data['n']
light_positions = np.array(data['light_positions'])
light_intensities = np.array(data['light_intensities'])
light_amb = data['Ia']
M = data['M']
N = data['N']
H = data['H']
W = data['W']
bg_color = data['bg_color']
f = data['focal']

mat_amb = PhongMaterial(ka, 0., 0., n)
mat_diff = PhongMaterial(0., kd, 0., n)
mat_spec = PhongMaterial(0., 0., ks, n)
mat_all = PhongMaterial(ka, kd, ks, n)

L = len(light_intensities)
lights = np.array([PointLight(light_positions[i], light_intensities[i]) for i in range(L)])


img_amb_gour = render_object('gouraud', f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vcolors, faces, mat_amb, lights, light_amb)
plt.figure()
plt.imshow(img_amb_gour, origin='lower')
plt.title('Gouraud shading with ambient lighting')
plt.savefig('Gouraud_Ambient.png', dpi=300)

img_diff_gour = render_object('gouraud', f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vcolors, faces, mat_diff, lights, light_amb)
plt.figure()
plt.imshow(img_diff_gour, origin='lower')
plt.title('Gouraud shading with diffuse lighting')
plt.savefig('Gouraud_Diffuse.png', dpi=300)

img_spec_gour = render_object('gouraud', f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vcolors, faces, mat_spec, lights, light_amb)
plt.figure()
plt.imshow(img_spec_gour, origin='lower')
plt.title('Gouraud shading with specular lighting')
plt.savefig('Gouraud_Specular.png', dpi=300)

img_gour = render_object('gouraud', f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vcolors, faces, mat_all, lights, light_amb)
plt.figure()
plt.imshow(img_gour, origin='lower')
plt.title('Gouraud shading with all lighting types')
plt.savefig('Gouraud_All.png', dpi=300)

img_amb_phong = render_object('phong', f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vcolors, faces, mat_amb, lights, light_amb)
plt.figure()
plt.imshow(img_amb_phong, origin='lower')
plt.title('Phong shading with ambient lighting')
plt.savefig('Phong_Ambient.png', dpi=300)

img_diff_phong = render_object('phong', f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vcolors, faces, mat_diff, lights, light_amb)
plt.figure()
plt.imshow(img_diff_phong, origin='lower')
plt.title('Phong shading with diffuse lighting')
plt.savefig('Phong_Diffuse.png', dpi=300)

img_spec_phong = render_object('phong', f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vcolors, faces, mat_spec, lights, light_amb)
plt.figure()
plt.imshow(img_spec_phong, origin='lower')
plt.title('Phong shading with specular lighting')
plt.savefig('Phong_Specular.png', dpi=300)

img_phong = render_object('phong', f, cam_eye, cam_lookat, cam_up, bg_color, M, N, H, W, verts, vcolors, faces, mat_all, lights, light_amb)
plt.figure()
plt.imshow(img_phong, origin='lower')
plt.title('Phong shading with all lighting types')
plt.savefig('Phong_All.png', dpi=300)