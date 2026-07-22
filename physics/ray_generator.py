import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import numpy as np

from physics.observer_tetrad import ObserverTetrad
from physics.null_photon import NullPhoton

class RayGenerator:
    """
    Converts camera rays into Schwarzschild
    photon initial conditions.
    """

    def __init__(self, black_hole):

        self.black_hole = black_hole

        self.tetrad = ObserverTetrad(
            black_hole
        )

    def generate(
        self,
        observer,
        direction
    ):
        #observer position
        r = observer.radius
        theta = observer.theta
        phi = observer.phi

        #normalize camera ray
        direction = direction / np.linalg.norm(direction)

        dx, dy, dz = direction

        #obtaining the tetrad
        basis = self.tetrad.basis(
            observer
        )

        #constructing a physically valid
        #null 4 momentum in the observer's inertial
        #frame

        local = NullPhoton.local_four_momentum(
            direction
        )

        print("direction =", direction)
        print("local =", local)

        # Transform from the observer's local frame
        # into Schwarzschild coordinates.

        k = (
            local[0] * basis["time"]
            + local[1] * basis["radial"]
            + local[2] * basis["theta"]
            + local[3] * basis["phi"]
        )

        print("e_r =", basis["radial"])

        #extractingt he components
        kt = k[0]

        kr = k[1]

        ktheta = k[2]

        kphi = k[3]

        #------Physics Check-------
        f = 1 - self.black_hole.schwarzschild_radius / r

        null = (
            -f * kt **2
            + kr**2 / f
            + (r**2) * ktheta **2
            + (r**2) * (np.sin(theta)**2) * kphi ** 2 
        )

        return np.array([

            0.0,
            r,
            theta,
            phi,

            kt,
            kr,
            ktheta,
            kphi

        ])