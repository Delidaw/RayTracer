import numpy as np

class SchwarzschildMetric:
    """
    Schwarzschild spacetime metric for non-rotating black hole.
    Coordinates:
       (t, r, θ, φ)
    """

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def metric_tensor(self, r, theta):
        """
        Returns the Schwarzschild metric tensor g_{μν} at given coordinates (r, θ).
        """
        
        R_s = self.black_hole.schwarzschild_radius

        f = 1 - R_s / r

        """
        [g_tt, g_rr, g_θθ, g_φφ]
        [g_tt, 0, 0, 0]     how time flows keeping radial, angular coordinates constant
        [0, g_rr, 0, 0]     how radial distance are stretched by spacetime curvature keeping time, angular coordinates constant
        [0, 0, g_θθ, 0]     g_θθ = r^2, how polar angle changes keeping time, radial coordinates constant
        [0, 0, 0, g_φφ]     g_φφ = r^2 * sin^2(θ), how azimuthal angle changes keeping time, radial coordinates constant
        """

        g = np.array([
            [-f,    0,      0,                       0],
            [ 0,  1/f,      0,                       0],
            [ 0,    0,   r**2,                       0],
            [ 0,    0,      0,  (r * np.sin(theta))**2]
        ])

        return g
    
    def inverse_metric(self, r,theta):
        """
        Returns the inverse of the Schwarzschild metric tensor 
        i.e., g^{μν} at given coordinates (r, θ).
        """
        
        R_s = self.black_hole.schwarzschild_radius

        f = 1 - R_s / r

        return np.array([
            [-1/f, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, 1/r**2, 0],
            [0, 0, 0, 1/(r**2*np.sin(theta)**2)]
    ])