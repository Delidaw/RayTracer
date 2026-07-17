import numpy as np


class RayGenerator:
    """
    Generates normalized camera-space ray
    directions from image pixels.
    """

    def __init__(self, camera, image_plane):

        self.camera = camera
        self.image_plane = image_plane

    def generate(self, pixel_x, pixel_y):
        """
        Generate the ray direction corresponding
        to a pixel.

        Returns
        -------
        ndarray
            Normalized direction vector (x, y, z).
        """

        # ----------------------------
        # Normalized pixel coordinates
        # ----------------------------

        u = (pixel_x + 0.5) / self.camera.width
        v = (pixel_y + 0.5) / self.camera.height

        # ----------------------------
        # Image plane coordinates
        # ----------------------------

        x = (u - 0.5) * self.image_plane.width

        y = (0.5 - v) * self.image_plane.height

        z = self.image_plane.distance

        direction = np.array([x, y, z])

        direction /= np.linalg.norm(direction)

        return direction