import numpy as np

class FrameDragging:
    """
    Computes the local frame-dragging angular velocity
    (Lense-Thirring effect) in Kerr spacetime.
    """

    def __init__(self, metric):
        self.metric = metric

    def omega(self, r, theta):
        """
        Frame dragging angular velocity Ω.
        
        Parameters
        -----------
        r : float
        theta : float
        
        Returns 
        -------
        float 
        """

        a = self.metric.black_hole.spin
        R_s = self.metric.black_hole.schwarzschild_radius

        cos = np.cos(theta)
        sin = np.sin(theta)

        sigma = r ** 2 + a ** 2 * cos ** 2

        delta = r ** 2 - R_s * r + a ** 2

        A = (
            (r ** 2 + a ** 2) ** 2
            - a ** 2 * delta * sin ** 2
        )

        return (R_s * a * r) / A