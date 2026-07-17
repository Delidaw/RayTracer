import numpy as np

class PhotonSphere:
    """
    Computes photon sphere properties for a metric.

    Currently supports Schwarzschild.
    Designed to be extended for Kerr.
    """

    def __init__(self, metric):
        self.metric = metric

    def radius(self):
        """
        Returns the photon sphere radius.
        """

        M = self.metric.M
        return 3.0 * M
    
    def is_inside(self, r):
        return r < self.radius()
    
    def is_outside(self, r):
        return r > self.radius()
    
    def is_on(self, r, tol=1e-6):
        return np.isclose(r, self.radius(), atol=tol)
    
