import numpy as np


class DiskShader:
    """
    Computes the brightness of the accretion disk.
    """

    def __init__(self, disk, black_hole):
        self.disk = disk
        self.black_hole = black_hole

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

        v_los = -np.sin(phi)

        doppler = 1.0 + 0.4 * v_los

        brightness *= doppler

        brightness = np.clip(
            brightness,
            0,
            255
        )

        colour = self.temperature_to_rgb(
            temperature
        )

        colour = (
            colour.astype(float)
            * brightness / 255
        )

        # ------------------------------------
        # Gravitational redshift
        # ------------------------------------

        M = self.black_hole.mass

        g = np.sqrt(
            max(
                1e-6,
                1 - 2 * M / r
            )
        )

        if v_los > 0:
            #approaching
            colour[2] *= 1.25 #blue
            colour[1] *= 1.10

        else:
            #receding
            colour[0] *= 1.15 #red
            colour[2] *= 0.70

        colour = np.clip(
            colour, 
            0,
            255
        )

        colour[0] *= 1.0
        colour[1] *= g
        colour[2] *= g * g

        colour = np.clip(
            colour,
            0,
            255
        )

        return colour.astype(np.uint8)

    def temperature_to_rgb(self, temperature):
        """
        Converts a normalized temperature (0–1)
        into an approximate accretion disk colour.

        0 -> cool (red)
        1 -> hot (white)
        """

        temperature = np.clip(
            temperature,
            0.0,
            1.0
        )

        red = 255

        green = int(
            120 + 135 * temperature
        )

        blue = int(
            40 + 170 * temperature
        )

        return np.array(
            [
                red,
                green,
                blue    
            ],
            dtype=np.uint8
        )