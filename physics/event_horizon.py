import numpy as np

class EventHorizon:
    """
    Computes the Kerr event horizon.
    """

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def radius(self):
        """
        Outer event horizon.
        r = M + sqrt(M² - a²)
        """

        M = self.black_hole.mass
        a = self.black_hole.spin

        r = M + np.sqrt(M ** 2 - a ** 2)

        return r