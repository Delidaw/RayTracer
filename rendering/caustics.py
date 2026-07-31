import numpy as np


class Caustics:
    """
    Approximate Kerr caustic magnification.

    Rays passing close to the photon region
    receive an additional brightness boost.
    """

    def __init__(self, black_hole):

        self.black_hole = black_hole
        self.max_boost = 2.5
        

    def magnification(self, trajectory):

        r = trajectory[:,1]

        r_min = np.min(r)

        scale = 2.0 + self.black_hole.spin

        boost = 1.0 + np.exp(
            -(r_min - scale)
        )

        return min(boost, self.max_boost)