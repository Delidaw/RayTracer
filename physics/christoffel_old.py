import numpy as np

class ChristoffelSymbols:
    """
    Computes the non-zero Christoffel symbols
    for Schwarzschild spacetime.
    """

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def compute(self, r, theta):

        R_s = self.black_hole.schwarzschild_radius

        f = 1 - R_s / r

        # gamma[λ][μ][ν]
        gamma = np.zeros((4, 4, 4))

        # Γ^t_tr = Γ^t_rt
        gamma[0, 0, 1] = R_s / (2 * r**2 * f)
        gamma[0, 1, 0] = gamma[0, 0, 1]

        # Γ^r_tt
        gamma[1, 0, 0] = R_s * f / (2 * r**2)

        # Γ^r_rr
        gamma[1, 1, 1] = -R_s / (2 * r**2 * f)

        # Γ^r_θθ
        gamma[1, 2, 2] = -r * f

        # Γ^r_φφ
        gamma[1, 3, 3] = -r * f * np.sin(theta)**2

        # Γ^θ_rθ = Γ^θ_θr
        gamma[2, 1, 2] = 1 / r
        gamma[2, 2, 1] = gamma[2, 1, 2]

        # Γ^φ_rφ = Γ^φ_φr
        gamma[3, 1, 3] = 1 / r
        gamma[3, 3, 1] = gamma[3, 1, 3]

        # Γ^θ_φφ
        gamma[2, 3, 3] = -np.sin(theta) * np.cos(theta)

        # Γ^φ_θφ = Γ^φ_φθ
        gamma[3, 2, 3] = 1 / np.tan(theta)
        gamma[3, 3, 2] = gamma[3, 2, 3]

        return gamma