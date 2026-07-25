import numpy as np


class DiskIntersector:
    """
    Determines whether a photon trajectory
    intersects the accretion disk.
    """

    def __init__(self, disk):
        self.disk = disk

    def intersects(self, trajectory):
        """
        Returns True if the photon crosses
        the accretion disk.
        """

        for state in trajectory:

            r = state[1]
            theta = state[2]

            # Near the equatorial plane
            near_plane = abs(theta - np.pi/2) < 0.02

            # Between disk radii
            inside_disk = (
                self.disk.inner_radius
                <= r
                <= self.disk.outer_radius
            )

            if near_plane and inside_disk:
                return True, state

        return False, None