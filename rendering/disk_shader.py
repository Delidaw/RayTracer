import numpy as np


class DiskShader:
    """
    Computes the brightness of the accretion disk.
    """

    def __init__(self, disk):
        self.disk = disk

    def shade(self, state):
        """
            Computes a simple radial brightness profile.

            Inner disk -> brighter
            Outer disk -> dimmer
        """

        r = state[1]

        inner = self.disk.inner_radius
        outer = self.disk.outer_radius

        # Clamp radius
        r = np.clip(r, inner, outer)

        # Brightness decreases linearly outward
        #brightness = 50 + 205 * (1 - (r - inner) / (outer - inner))

        temperature = (inner / r) ** 0.75

        brightness = 50 + 205 * temperature

        phi = state[3]

        doppler = 1.0 + 0.3 * np.cos(phi)

        brightness *= doppler

        brightness = np.clip(
            brightness,
            0,
            255
        )
        return np.uint8(brightness)