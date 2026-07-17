
import numpy as np
from physics.metric_derivatives import MetricDerivatives

class SchwarzschildDerivatives(MetricDerivatives):
    
    def __init__(self, metric):
        self.metric = metric

    def compute(self, r, theta):

        R_s = self.metric.event_horizon_radius()

        dg = np.zeros((4,4,4))

        # ∂g_tt / ∂r
        dg[1,0,0] = -R_s / r ** 2

        # ∂g_rr / ∂r
        dg[1,1,1] = -R_s / (r - R_s) ** 2

        # ∂g_θθ / ∂r
        dg[1,2,2] = 2 * r

        # ∂g_φφ / ∂r
        dg[1,3,3] = 2 * r * np.sin(theta) ** 2

        # ∂g_φφ / ∂θ
        dg[2,3,3] = 2 * r ** 2 * np.sin(theta) * np.cos(theta)

        return dg