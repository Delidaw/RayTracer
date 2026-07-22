import numpy as np

class KerrPhotonSphere:

    def __init__(self, black_hole):
        self.black_hole = black_hole

    @property
    def M(self):
        return self.black_hole.mass
    
    @property
    def a(self):
        return self.black_hole.spin

    def prograde(self):
        M = self.M
        a = self.a

        return 2 * M * (
            1 + np.cos(
                (2/3) * np.arccos(-a / M)
            )
        )

    def retrograde(self):
        M = self.M
        a = self.a

        return 2 * M * (
            1 + np.cos(
                (2/3) * np.arccos(a / M)
            )
        )        