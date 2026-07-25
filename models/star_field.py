import numpy as np

class StarField:
    """
    Represents a distant celestial sphere.
    
    Given a photon direction, 
    returns the background brightness.
    """

    def __init__(self, brightness = 255):
        self.brightness = brightness

    def sample(self, direction):
        """
        Sample the sky in a given direction.

        Parameters
        ----------
        direction : ndarray (3,)
            Unit direction vector.

        Returns
        -------
        int
            Pixel brightness.
        """

        return  self.brightness