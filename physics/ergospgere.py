import numpy as np

class Ergosphere:
    """
    Computes the outer ergosphere of a 
    Kerr blackhole.
    """

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def radius(self, theta):
        """
        Outer ergosphere radius. 
        
        Parameters 
        ----------
        theta : float 
        
        Return 
        ---------
        float
        """

        M = self.black_hole.mass
        a = self.black_hole.spin

        return M + np.sqrt(
            M ** 2 
            - a ** 2 * np.cos(theta) ** 2
        )