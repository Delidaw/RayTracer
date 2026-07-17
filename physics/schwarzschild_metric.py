import numpy as np

from physics.metric import Metric

class SchwarzschildMetric(Metric):
    """
    Schwarzschild spacetime metric for non-rotating black hole.
    Coordinates:
       (t, r, θ, φ)
    """
    # ==================================================
    # Future Work (Phase 3)
    # Embedding diagram of Schwarzschild spacetime
    # ==================================================

    def __init__(self, black_hole):

        super().__init__(black_hole.mass)
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

        return np.linalg.inv(self.metric_tensor(r, theta))

        """
        return np.array([
            [-1/f, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, 1/r**2, 0],
            [0, 0, 0, 1/(r**2*np.sin(theta)**2)]
    ])"""

    def event_horizon_radius(self):

        return self.black_hole.schwarzschild_radius

    # =========================================================
# Future Work (Phase 3)
# Spacetime Curvature Mesh
# =========================================================
#
# The following code will be used later to generate
# a 3D embedding diagram of Schwarzschild spacetime.
#
# r = np.linspace(R_s + 0.1, 50, 500)
#
# z = 2 * np.sqrt(R_s * (r - R_s))
#
# theta = np.linspace(0, 2 * np.pi, 500)
#
# R, Theta = np.meshgrid(r, theta)
#
# X = R * np.cos(Theta)
# Y = R * np.sin(Theta)
# Z = 2 * np.sqrt(R_s * (R - R_s))
#
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection="3d")
# ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
#
# ax.set_title("Schwarzschild Spacetime Embedding Diagram")
# ax.set_xlabel("X")
# ax.set_ylabel("Y")
# ax.set_zlabel("Curvature")
#
# plt.show()
#
# =========================================================