#legacy_camera.py


import numpy as np

class Camera:
    """
    Represents the observer's camera.
    """

    def __init__(
            self,
            observer,
            fov = 60,
            width = 800,
            height = 800
    ):
        self.observer = observer
        self.fov = fov

        self.width = width
        self.height = height


    def pixel_grid(self):
        """
        Returns normalized image-plane coordinates.

        Returns
        -------
        X, Y : 2D arrays
        Coordinates ranging from -1 to +1.
    
        """

        half_size = np.tan(np.radians(self.fov) / 2)

        x = np.linspace(
            -half_size,
            half_size,
            self.width
        )

        y = np.linspace(
            -half_size,
            half_size,
            self.width
        )

        X, Y = np.meshgrid(x, y)

        return X, Y
    
    def ray_directions(self):
        """
        Generate one normalized ray direction
        for every pixel.
        
        
        Returns 
        -------
        directions : nd.array
            Shape = (height, width, 3)
        """

        X, Y = self.pixel_grid()

        Z = np.ones_like(X)

        directions = np.stack(
            (X, Y, Z),
            axis = -1
        )

        norms = np.linalg.norm(
            directions,
            axis = -1,
            keepdims = True
        )
        
        directions /= norms

        return directions

