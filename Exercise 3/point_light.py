import numpy as np


class PointLight:
    # Class that represents a light source at a certain position with an intensity represented in RGB format
    def __init__(self, pos, intensity):
        # Constructor
        # Vector validation
        self._validate_vector(pos, (3,)) 
        self._validate_vector(intensity, (3,))
        self.pos = pos # Source's coordinates in the WCS
        self.intensity = intensity # Source's RGB color intensity
        # Check that all color coefficients of the source's light are in the [0, 1] interval
        if not np.all((intensity >= 0) & (intensity <= 1)):
            raise ValueError("Intensity values must be in the [0, 1] interval")
    
    def _validate_vector(self, vector, shape):
        # Function that validates that all parameters of the class are vectors of the required shape
        if vector.shape != shape or not isinstance(vector, np.ndarray):
            raise ValueError(f"Vector shape must be {shape} NDArray")
        
    