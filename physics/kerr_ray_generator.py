import numpy as np

from physics.kerr_observer_tetrad import KerrObserverTetrad
from physics.null_photon import NullPhoton

class KerrRayGenerator:
    """
    Converts camera rays into Kerr photon
    initial conditions.
    """

    def __init__(self, metric):

        self.metric = metric

        self.tetrad = KerrObserverTetrad(metric)

    def generate(
        self,
        observer,
        direction
    ):
        r = observer.radius
        theta = observer.theta
        phi = observer.phi

        direction = direction / np.linalg.norm(direction)

        local = NullPhoton.local_four_momentum(direction)

        basis = self.tetrad.basis(observer)

        k = (
            local[0] * basis["time"]
            + local[1] * basis["radial"]
            + local[2] * basis["theta"]
            + local[3] * basis["phi"]
        )

        print("kt =", k[0])
        print("kr =", k[1])
        print("ktheta =", k[2])
        print("kphi =", k[3])

        kt = k[0]
        kr = k[1]
        ktheta = k[2]
        kphi = k[3]

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