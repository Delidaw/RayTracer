import numpy as np


class HDRBuffer:
    """
    Stores floating-point colour values before
    tone mapping.
    """

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.buffer = np.zeros(
            (height, width, 3),
            dtype=np.float32
        )

    def write(
        self,
        row,
        col,
        colour
    ):

        self.buffer[row, col] = colour.astype(
            np.float32
        )

    def image(self):

        return self.buffer