import numpy as np
import matplotlib.image as mpimg


class StarField:

    """
    Represents a celestial sphere.

    Rays escaping the black hole sample
    this texture.
    """

    def __init__(self, texture_path):

        self.texture = mpimg.imread(texture_path)

        if self.texture.dtype != np.uint8:
            self.texture = (255 * self.texture).astype(np.uint8)

        self.height = self.texture.shape[0]
        self.width = self.texture.shape[1]

    def sample(self, direction):
        """
        Sample the celestial sphere using bilinear interpolation.
        """

        direction = direction / np.linalg.norm(direction)

        x, y, z = direction

        phi = np.arctan2(y, x)
        theta = np.arccos(z)

        u = (phi + np.pi) / (2 * np.pi)
        v = theta / np.pi

        # Floating-point texture coordinates
        x_tex = u * (self.width - 1)
        y_tex = v * (self.height - 1)

        x0 = int(np.floor(x_tex))
        y0 = int(np.floor(y_tex))

        x1 = (x0 + 1) % self.width      # wrap horizontally
        y1 = min(y0 + 1, self.height - 1)   # clamp vertically

        dx = x_tex - x0
        dy = y_tex - y0

        c00 = self.texture[y0, x0].astype(np.float32)
        c10 = self.texture[y0, x1].astype(np.float32)
        c01 = self.texture[y1, x0].astype(np.float32)
        c11 = self.texture[y1, x1].astype(np.float32)

        top = (1.0 - dx) * c00 + dx * c10
        bottom = (1.0 - dx) * c01 + dx * c11

        colour = (1.0 - dy) * top + dy * bottom

        return colour.astype(np.uint8) / 255.0