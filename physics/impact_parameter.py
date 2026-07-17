import numpy as np

class ImpactParameter:
    """
    Computes and classifies photon impact parameters
    in Schwarzschild spacetime.
    """

    def __init__(self,black_hole):
        self.black_hole = black_hole

    def critical(self):
        """
        Returns the critical impact parameter

            b_c = 3√3 M
        """
        M = self.black_hole.mass
        return 3 * np.sqrt(3) * M
    
    def classify(self, impact_parameter):
        bc = self.critical()
        b = impact_parameter

        tol = 1e-6 #Floating-point arithmetic is not exact.

        if abs(b - bc) < tol:
            return "critical"
        
        elif b < bc:
            return "capture"
        
        else:
            return "escape"
        
