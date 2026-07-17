import numpy as np


class NullPhoton:
    """
    Constructs physically valid null four-momentum
    in the observer's local orthonormal frame.
    """

    @staticmethod
    def local_four_momentum(direction):
        """
        Parameters
        ----------
        direction : ndarray(3,)
            Unit spatial direction.

        Returns
        -------
        ndarray(4,)
            Null four-momentum in the observer frame.
        """

        direction = direction / np.linalg.norm(direction)

        px, py, pz = direction

        return np.array([
            1.0,

            -pz,   # radial

             py,   # theta

             px    # phi
        ])