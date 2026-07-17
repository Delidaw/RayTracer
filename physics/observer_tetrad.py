import numpy as np

class ObserverTetrad:
    """
    Constructs an orthonormal tetrad for a 
    stationary observer in Schwarzschild 
    spacetime.

    The tetrad converts vectors between:

    Local observer frame <--> Schwarzschild coordinates
    """

    def __init__(self, black_hole):

        self.black_hole = black_hole

    def schwarzschild_factor(self, radius):
        """
        Returns 
        
        f = 1 - Rs/r

    appearing in the Schwarzschild metric.
    """
        
        return 1 - (
            self.black_hole.schwarzschild_radius
            / radius
        )
    
    def basis(self, observer):

        """
        Constructs the observer's orthonormal tetrad.

    Returns
    -------
    dict
        Local basis vectors expressed in
        Schwarzschild coordinates.
        """

        r = observer.radius
        theta = observer.theta

        f = self.schwarzschild_factor(r)

        #Time basis vector
        e_t = np.array([
            1 / np.sqrt(f),
            0,
            0,
            0
        ])

        #Radial Basis
        e_r = np.array([
            0,
            np.sqrt(f),
            0,
            0
        ])

        #Theta Basis
        e_theta = np.array([
            0,
            0,
            1 / r,
            0
        ])

        #Phi BAsis
        e_phi = np.array([
            0,
            0,
            0,
            1 / (r * np.sin(theta))
        ])

        return {
            "time": e_t,
            "radial": e_r,
            "theta": e_theta,
            "phi": e_phi
        }