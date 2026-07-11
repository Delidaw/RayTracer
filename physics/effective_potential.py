import numpy as np

class EffectivePotential:

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def particle(self, radius, angular_momentum):
        """
        Schwarzschild effective potential
        for massive particle.
        """

        M = self.black_hole.schwarzschild_radius / 2

        f = 1 - (2 * M / radius)

        return f * (
            1
            + angular_momentum**2 / radius **2
        )