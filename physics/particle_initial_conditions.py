"""
import numpy as np

class ParticleInitialConditions:
    "
    Generates physically consistent initial states
    for massive particles in Schwarzschild spacetime.
    "

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def radial_infall(self, radius):

        R_s = self.black_hole.schwarzschild_radius

        if radius <= R_s:
            raise ValueError(
                "Particle must start outside the event horizon."
            )

        ut = 1.0 / np.sqrt(1 - R_s / radius)

        return np.array([
            0.0,
            radius,
            np.pi / 2,
            0.0,

            ut,
            0.0,
            0.0,
            0.0
        ])

    def escape_trajectory(self, radius, speed):
        "
        Particle launched outward with an initial radial speed.
        "
        pass

    def elliptical_orbit(self, radius, eccentricity):
        "
        Particle placed on an elliptical orbit.
        "
        pass
"""