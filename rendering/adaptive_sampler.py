import numpy as np


class AdaptiveSampler:
    """
    Determines how many rays should
    be traced for each pixel.
    """

    def __init__(self):

        self.default_samples = 1
        self.edge_samples = 4

        #centre + four corners
        self.offsets = np.array([
            (0.0, 0.0),
            (-0.25, -0.25),
            (0.25, -0.25),
            (-0.25, 0.25),
            (0.25, 0.25)
        ])

    def samples(self, colour):

        variance = np.std(colour)

        if variance > 40:
            return self.edge_samples

        return self.default_samples