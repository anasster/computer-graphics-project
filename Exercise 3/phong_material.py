import numpy as np


class PhongMaterial:
    # Class that contains the coefficients of a 3D surface's material according to the phong shading model.    
    def __init__(self, ka, kd, ks, n):
        # Constructor function
        self._validate_data_types(ka, kd, ks, n) # Data type validation
        self.ka = ka # Ambient lighting coefficient 
        self.kd = ks # Diffuse reflection coefficient
        self.ks = ks # Specular reflection coefficient
        self.n = n # Phong coefficient
        
    def _validate_data_types(self, ka, kd, ks, n):
        # Function that checks if all the parameters are of the requred data type
        if not isinstance(ka, float):
            raise TypeError("ka must be a float")
        if not isinstance(kd, float):
            raise TypeError("kd must be a float")
        if not isinstance(ks, float):
            raise TypeError("ks must be a float")
        if not isinstance(n, int):
            raise TypeError("n must be a positive integer")
    
   
    