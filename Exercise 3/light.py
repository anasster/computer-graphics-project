import numpy as np
from phong_material import *
from point_light import *


def light(point, normal, color, cam_pos, mat, lights, light_amb):
    # Function that colors a 3D point according to the Phong model (uses CCS coordinates)
    v = (cam_pos - point) / np.linalg.norm(cam_pos - point) # Unitary vector pointing from the point to the viewer
    
    I = np.zeros(3)
    ambient = mat.ka * color * light_amb # Ambient lighting
    for light in lights:
        # Define vector from point to light source
        l = light.pos - point / np.linalg.norm(light.pos - point)
        l = l/np.linalg.norm(l)
        
        diffuse = mat.kd * color * light.intensity * np.dot(normal, l) # Diffuse formula
        specular = mat.ks * color * light.intensity * np.power(np.dot(2 * normal * np.dot(normal, l) - l, v), mat.n) # Specular formula
        I += diffuse + specular

    I += ambient 
    I = np.clip(I, 0, 1) # The final color (i.e. the sum of each illumination technique) contained in the [0, 1] interval
    return I
