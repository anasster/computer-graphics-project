import numpy as np
import matplotlib.pyplot as plt
from rot_mat import *
from rotate_translate import *
from change_coordinate_system import *
from render_object import *
import time


s = time.time()
data = np.load('h2.npy', allow_pickle=True, encoding='ASCII').item()
verts3d = data['verts3d'].T
faces = data['faces']
vcolors = data['vcolors']
u = data['u']
phi = data['phi']
t1 = data['t_1']
t2 = data['t_2']
cCam = np.squeeze(data['c_org'])
cLookAt = np.squeeze(data['c_lookat'])
cUp = np.squeeze(data['c_up'])
f = data['focal']
p2d, depth = camera_looking_at(f, cCam, cLookAt, cUp, verts3d)
h = 15
w  = 15
rows = 512
cols = 512
# Step 0: Produce the 2D image
img = render_object(verts3d, faces, vcolors, h, w, rows, cols, f, cCam, cLookAt, cUp)
plt.figure()
plt.imshow(img)
plt.xlabel('Width')
plt.ylabel('Height')
plt.title('Step 0: Rendering')
plt.savefig('step0.jpg', dpi=300)

# Step I: Translate by t1
verts3d = rotate_translate(verts3d, 0, u, cLookAt, t1)
img = render_object(verts3d, faces, vcolors, h, w, rows, cols, f, cCam, cLookAt, cUp)
plt.figure()
plt.imshow(img)
plt.xlabel('Width')
plt.ylabel('Height')
plt.title('Step I: Translation by t1')
plt.savefig('step1.jpg', dpi=300)

# Step II: Rotate by phi radians
verts3d = rotate_translate(verts3d, phi, u, cLookAt, np.zeros(3))
img = render_object(verts3d, faces, vcolors, h, w, rows, cols, f, cCam, cLookAt, cUp)
plt.figure()
plt.imshow(img)
plt.xlabel('Width')
plt.ylabel('Height')
plt.title('Step II: Rotation by phi radians around axis parallel to vector u')
plt.savefig('step2.jpg', dpi=300)

# Step III: Translate by t2
verts3d = rotate_translate(verts3d, 0, u, cLookAt, t2)
img = render_object(verts3d, faces, vcolors, h, w, rows, cols, f, cCam, cLookAt, cUp)
plt.figure()
plt.imshow(img)
plt.xlabel('Width')
plt.ylabel('Height')
plt.title('Step III: Translation by t2')
plt.savefig('step3.jpg', dpi=300)

e = time.time()
ex = e - s
print(f"Execution time: {ex} s")
