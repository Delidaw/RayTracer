import numpy as np

class KerrISCO:

    def __init__(self, black_hole):
        self.black_hole = black_hole

    @property
    def M(self):
        return self.black_hole.mass
    
    @property
    def a(self):
        return self.black_hole.spin
    
    #Auxiliary quantities
    @property
    def Z1(self):
        M = self.M
        a = self.a

        return (
            1
            + (1 - (a / M) ** 2)**(1/3)
            * (
                (1 + a / M) ** (1 / 3)
                + (1 - a / M) ** (1 / 3)
            )
        )
    
    @property
    def Z2(self):

        return np.sqrt(
            3 * (self.a / self.M) ** 2
            + self.Z1 ** 2
        )
    
    #Bardeen Formula for prograde ISCO
    def prograde(self):

        M = self.M

        return M * (
            3 
            + self.Z2
            - np.sqrt(
                (3 - self.Z1)
                * (
                    3 
                    + self.Z1
                    + 2 * self.Z2
                )
            )
        )
    
    #Bardeen Formula for Retrograde ISCO
    def retrograde(self):
        M = self.M

        return M * (
            3 
            + self.Z2
            + np.sqrt(
                (3 - self.Z1)
                * (
                    3
                    + self.Z1
                    + 2 * self.Z2
                )
            )
        )