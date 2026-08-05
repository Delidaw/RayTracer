import numpy as np


class LensingMapper:
    """
    Converts the final escaping photon momentum
    into a direction on the celestial sphere.
    """

    def direction(self, trajectory):

        state = trajectory[-1]

        kr = state[5]
        ktheta = state[6]
        kphi = state[7]

        direction = np.array(
            [
                kr,
                ktheta,
                kphi
            ],
            dtype=np.float64
        )

        norm = np.linalg.norm(direction)

        if norm == 0 or not np.isfinite(norm):
            return np.array(
                [0.0, 0.0, 1.0],
                dtype=np.float64
            )

        return direction / norm