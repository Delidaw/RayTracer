
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
            self.height
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

    def ray_direction(self, x, y):
        """
        Generate a normalized ray direction for a single pixel
        or subpixel coordinate.
        """

        half_size = np.tan(
            np.radians(self.fov) / 2
        )

        px = -half_size + (
            2.0 * half_size * x / self.width
        )

        py = -half_size + (
            2.0 * half_size * y / self.height
        )

        direction = np.array(
            [px, py, 1.0],
            dtype=np.float64
        )

        direction /= np.linalg.norm(direction)

        return direction

    @property 
    def aspect_ratio(self):
        return self.width / self.height

