import numpy as np

from physics.metric import Metric

class KerrMetric(Metric):

    def __init__(self, black_hole):

        super().__init__(black_hole.mass)

        self.black_hole = black_hole


    def sigma(self, r, theta):
        """
        Σ = r² + a² cos²θ
        """

        a = self.black_hole.spin

        return r ** 2 + a ** 2 * np.cos(theta) ** 2
    
    def delta(self, r):
        """
        Δ = r² - 2Mr + a²
        """

        M = self.black_hole.mass
        a = self.black_hole.spin

        return r ** 2 - 2 * M * r + a ** 2
    
    def metric_tensor(self, r, theta):
        Sigma = self.sigma(r, theta)

        Delta = self.delta(r)

        M= self.black_hole.mass

        a = self.black_hole.spin

        g_tt = -(1 - (2 * M * r) / Sigma)

        g_rr = Sigma / Delta

        g_thetatheta = Sigma

        g_tphi = - 2 * M * a * r * np.sin(theta) ** 2 / Sigma

        g_phiphi = (r ** 2 + a ** 2 + (2 * M * a ** 2 * r * np.sin(theta) ** 2) / Sigma) * (np.sin(theta) ** 2)

        g = np.array([
            [g_tt,   0,    0,            g_tphi],
            [0,      g_rr, 0,            0],
            [0,      0,    g_thetatheta, 0],
            [g_tphi, 0,    0,            g_phiphi]
        ])

        return g
    
    def inverse_metric(self, r, theta):
        g = self.metric_tensor(r, theta)
        return np.linalg.inv(g)

    def event_horizon_radius(self):

        M = self.black_hole.mass
        a = self.black_hole.spin

        r = M + np.sqrt(M ** 2 - a ** 2)
        return r