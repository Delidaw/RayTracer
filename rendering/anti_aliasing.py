import numpy as np


class AntiAliasing:

    """
    Generates sub-pixel offsets for
    supersampling.
    """

    def __init__(self):

        self.offsets = np.array([
            [-0.25, -0.25],
            [ 0.25, -0.25],
            [-0.25,  0.25],
            [ 0.25,  0.25]
        ])

    def samples(self):

        return self.offsets