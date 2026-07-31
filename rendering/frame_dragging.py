import numpy as np


class FrameDragging:
    """
    Estimates how strongly a photon
    experiences Kerr frame dragging.
    """

    def __init__(self):

        self.max_boost = 1.4

    def boost(self, trajectory):

        phi = trajectory[:,3]

        twist = np.sum(
            np.abs(
                np.diff(phi)
            )
        )

        boost = 1 + min(
            self.max_boost - 1,
            twist / (4*np.pi)
        )

        return boost