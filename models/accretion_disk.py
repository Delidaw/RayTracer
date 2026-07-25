import numpy as np

class AccretionDisk:
    """
    Thin accretion disk around the black hole.
    """

    def __init__(
            self,
            inner_radius,
            outer_radius,
            brightness = 200
    ):
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.brightness = brightness

    def contains(self, radius):
        """
        Returns True if the point lies inside the disk.
        """

        return(
            self.inner_radius
            <= radius
            <= self.outer_radius
        )