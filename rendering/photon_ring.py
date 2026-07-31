import numpy as np


class PhotonRing:
    """
    Detects photons that orbit the black hole
    before escaping.

    These photons are slightly brightened,
    producing the characteristic photon ring.
    """

    def __init__(self):

        self.ring_angle = np.pi
        self.max_boost = 1.8

    def brightness(self, trajectory):

        if len(trajectory) < 2:
            return 1.0

        phi = trajectory[:, 3]

        total_angle = np.sum(
            np.abs(
                np.diff(phi)
            )
        )

        if total_angle < self.ring_angle:
            return 1.0

        boost = 1.0 + min(
            self.max_boost - 1.0,
            (total_angle - self.ring_angle) / np.pi
        )

        return boost