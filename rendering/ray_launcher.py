import numpy as np


class RayLauncher:
    """
    Converts a camera-space ray direction into a
    Schwarzschild-coordinate photon state.
    """

    def __init__(self, observer, tetrad):

        self.observer = observer
        self.tetrad = tetrad

    def launch(self, direction):
        """
        Parameters
        ----------
        direction : ndarray
            Normalized camera-space direction (x,y,z).

        Returns
        -------
        ndarray
            Initial photon state vector.
        """

        basis = self.tetrad.basis(self.observer)

        dx, dy, dz = direction

        # Local photon four-momentum
        k_local = np.array([
            1.0,
            -dz,
            dy,
            dx
        ])

        e_t = basis["time"]
        e_r = basis["radial"]
        e_theta = basis["theta"]
        e_phi = basis["phi"]

        k_coord = (
            k_local[0] * e_t
            + k_local[1] * e_r
            + k_local[2] * e_theta
            + k_local[3] * e_phi
        )

        return np.array([
            0.0,
            self.observer.radius,
            self.observer.theta,
            self.observer.phi,

            k_coord[0],
            k_coord[1],
            k_coord[2],
            k_coord[3]
        ])