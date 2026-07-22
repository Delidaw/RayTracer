import numpy as np

from physics.christoffel import ChristoffelSymbols
from physics.metric import Metric


class GeodesicEquation:

    def __init__(self, metric, derivatives):

        self.metric = metric
        self.metric_derivatives = derivatives
        self.connection = ChristoffelSymbols(metric, derivatives)

    def derivatives(self, state):
        """
        This function receives
        state =
        [t, r, θ, φ, ut, ur, uθ, uφ ]
        first 4 coordinates,
        last 4 are the corresponding 4-velocities(u)
        """

        t, r, theta, phi, ut,ur, uθ, uφ = state

        gamma = self.connection.compute(r, theta)

        velocity = np.array([ut, ur, uθ, uφ])

        acceleration = np.zeros(4)

        #translating einstein equation into python
        #−Γλ_μν * ​uμ * uν
        #uμ=dxμ​ / dτ
        for lam in range(4):
            for mu in range(4):
                for nu in range(4):
                    acceleration[lam] -= (
                        gamma[lam, mu, nu] 
                        * velocity[mu] 
                        * velocity[nu]
                    )

        print("-------------------------")
        print("r =", r)
        print("ur =", ur)
        print("uphi =", uφ)

        print("ar =", acceleration[1])
        print("aphi =", acceleration[3])

        return np.array([
            ut, 
            ur, 
            uθ, 
            uφ, 

            acceleration[0], 
            acceleration[1], 
            acceleration[2], 
            acceleration[3]
        ])