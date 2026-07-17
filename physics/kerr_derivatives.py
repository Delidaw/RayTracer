import numpy as np

from physics.metric_derivatives import MetricDerivatives

class KerrDerivatives(MetricDerivatives):

    def __init__(self, metric):
        self.metric = metric

    def compute(self, r, theta):
        M = self.metric.black_hole.mass
        a = self.metric.black_hole.spin

        Sigma = self.metric.sigma(r, theta)
        Delta = self.metric.delta(r)

        dSigma_dr = 2 * r
        dSigma_dtheta = -2 * a ** 2 * np.sin(theta) * np.cos(theta)

        dDelta_dr = 2 * r - 2 * M
        dDelta_dtheta = 0.0

        dg = np.zeros((4,4,4))

        ## ∂g_tt / ∂r
        dg[1,0,0] = (
            2 * M * (Sigma - 2 * r**2)
            / Sigma**2
        )

        # ∂g_tt / ∂θ
        dg[2,0,0] = (
            -2 * M * r * dSigma_dtheta
            / Sigma**2
        )

        # ∂g_rr / ∂r
        dg[1,1,1] = (
            Delta * dSigma_dr
            - Sigma * dDelta_dr
        ) / Delta**2

        # ∂g_rr / ∂θ
        dg[2,1,1] = (
            dSigma_dtheta
        ) / Delta

        # ∂g_tϕ / ∂r
        N = 2 * M * a * r * np.sin(theta) ** 2

        dN_dr = 2 * M * a * np.sin(theta) ** 2

        dg[1,0,3] = -(
            Sigma * dN_dr
            - N * dSigma_dr
        ) / Sigma ** 2

        #∂g_tϕ / ∂θ
        dN_dtheta = 4 * M * a * r * np.sin(theta) * np.cos(theta)

        dg[2,0,3] = -(
            Sigma * dN_dtheta
            - N * dSigma_dtheta
        ) / Sigma ** 2

        dg[2,3,0] = dg[2,0,3]


        #∂g_θθ / ∂r
        dg[1,2,2] = dSigma_dr

        #∂g_θθ / ∂θ
        dg[2,2,2] = dSigma_dtheta


        #∂g_ϕϕ / ∂r
        A = 2 * M * a**2 * r * np.sin(theta)**2

        dA_dr = 2 * M * a**2 * np.sin(theta)**2

        dg[1,3,3] = (
            2*r
            + (Sigma*dA_dr - A*dSigma_dr)/Sigma**2
        ) * np.sin(theta)**2

        #∂g_ϕϕ / ∂θ
        S = np.sin(theta)**2

        A = 2 * M * a**2 * r * S

        g_phiphi = (r**2 + a**2 + A/Sigma) * S

        dS_dtheta = np.sin(2*theta)

        dA_dtheta = (
            2*M*a**2*r*dS_dtheta
        )

        dQuotient = (
            Sigma*dA_dtheta
            - A*dSigma_dtheta
        )/Sigma**2

        dg[2,3,3] = (
            dS_dtheta
            * (
                r**2
                + a**2
                + A/Sigma
            )
            +
            S*dQuotient
        )


        print("dg[r,t,t] =", dg[1,0,0])
        print("dg[theta,t,t] =", dg[2,0,0])

        print("dg[r,r,r] = ", dg[1,1,1])
        print("dg[theta,r,r] = ", dg[2,1,1])

        print("dg[r,t,phi] = ", dg[1,0,3])
        print("dg[theta,t,phi] = ", dg[2,0,3])

        print("dg[r,theta,theta] =", dg[1,2,2])
        print("dg[theta,theta,theta] =", dg[2,2,2])

        print("dg[r,phi,phi] =", dg[1,3,3])
        print("dg[theta,phi,phi] =", dg[2,3,3])

        

        
        """
        print("Sigma =", Sigma)
        print("Delta =", Delta)
        print("dSigma_dr =", dSigma_dr)
        print("dSigma_dtheta =", dSigma_dtheta)
        print("dDelta_dr =", dDelta_dr)
        print("dDelta_dtheta =", dDelta_dtheta)
        """

        return dg