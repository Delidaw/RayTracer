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

        direction = direction / np.linalg.norm(direction)

        x, y, z = direction

        phi = np.arctan2(y, x)

        theta = np.arccos(z)

        u = (phi + np.pi) / (2 * np.pi)

        v = theta / np.pi

        column = int(u * (self.width - 1))
        row = int(v * (self.height - 1))

        return self.texture[row, column]