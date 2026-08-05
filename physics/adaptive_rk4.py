import numpy as np


class AdaptiveRK4:
    """
    Computes an adaptive RK4 step size.

    Smaller steps are used near the black hole,
    while larger steps are used farther away.
    """

    def __init__(
        self,
        minimum_step=0.002,
        maximum_step=0.05,
        photon_radius=3.0,
    ):
        self.minimum_step = minimum_step
        self.maximum_step = maximum_step
        self.photon_radius = photon_radius

    def step_size(self, r):
        """
        Choose an RK4 step size based on radius.
        """

        if r <= self.photon_radius:
            return self.minimum_step

        t = min((r - self.photon_radius) / 17.0, 1.0)

        return (
            self.minimum_step +
            t * (self.maximum_step - self.minimum_step)
        )