import numpy as np

class Observer:
    """
     Represents an observer located in Schwarzschild spacetime.

    The observer is the point from which all photons are launched
    during ray tracing.
    """

    def __init__(
            self,
            radius,
            theta = np.pi / 2,
            phi = 0.0
    ):
        self.radius = radius
        self.theta = theta
        self.phi = phi

    @property
    def position(self):
        """
        Returns observer position in Schwarzschild coordinates.
        """

        return np.array([
            self.radius,
            self.theta,
            self.phi
        ])