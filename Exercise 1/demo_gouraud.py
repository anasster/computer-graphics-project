import numpy as np
from render import render
import matplotlib.pyplot as plt
import time

start_time = time.time()
data = np.load('h1.npy', allow_pickle=True, encoding='latin1').item()
m = 512
n = 512

verts2d = data['verts2d']
faces = data['faces']
vcolors = data['vcolors']
depth = data['depth']

image = render(verts2d, faces, vcolors, depth,  'gouraud')

end_time = time.time()
ex_time = end_time - start_time
print(f"Execution time: {ex_time:4f} s")

plt.imshow(image)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Gouraud Shaded Object")
plt.show()