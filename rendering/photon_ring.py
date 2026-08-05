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
        """
        Brighten photons that complete one or more
        revolutions around the black hole.
        """

        if len(trajectory) < 2:
            return 1.0

        phi = trajectory[:, 3]

        # Remove discontinuities at ±π
        phi = np.unwrap(phi)

        total_angle = np.abs(phi[-1] - phi[0])

        revolutions = total_angle / (2.0 * np.pi)

        if revolutions < 0.5:
            return 1.0

        boost = 1.0 + min(
            self.max_boost - 1.0,
            revolutions * 0.4
        )

        return boost