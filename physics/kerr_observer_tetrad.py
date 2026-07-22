import numpy as np

class KerrObserverTetrad:
    """
    Local orthonormal frame for a stationary observer
    in Kerr spacetime.
    """

    def __init__(self, metric):

        self.metric = metric

        self.black_hole = metric.black_hole

    #validated inside validation/validate_kerr_tetrad.py

    @property
    def M(self):
        return self.black_hole.mass


    @property
    def a(self):
        return self.black_hole.spin
    
    def sigma(self, r, theta):

        return (
            r**2
            + self.a**2 * np.cos(theta)**2
        )
    
    def delta(self, r):

        return (
            r**2
            - 2*self.M*r
            + self.a**2
        )
    

    #Validated inside validation/validate_kerr_metric_coefficients.py
    
    #g_tt
    def g_tt(self, r, theta):

        sigma = self.sigma(r, theta)

        return -(1 - (2 * self.M * r) / sigma)
    
    #g_tphi
    def g_tphi(self, r, theta):

        sigma = self.sigma(r, theta)

        return (
            -2 * self.M * self.a * r
            * np.sin(theta) ** 2
            / sigma
        )
    
    #g_rr
    def g_rr(self, r, theta):
        return self.sigma(r, theta) / self.delta(r)
    
    #g_theta theta
    def g_thetatheta(self, r, theta):
        return self.sigma(r, theta)
    
    #g_phi phi
    def g_phiphi(self, r, theta):
        sigma = self.sigma(r, theta)

        sin2 = np.sin(theta) ** 2

        return (
            (
                r ** 2
                + self.a ** 2
                + (
                    2 * self.M * self.a ** 2 * r * sin2
                    / sigma
                )
            )
            *sin2
        )
    
    #validated inside validation/validate_kerr_spatial_basis.py

    def e_r(self, r, theta):

        return np.array([
            0.0,
            1 / np.sqrt(self.g_rr(r, theta)),
            0.0,
            0.0
        ])
    
    def e_theta(self, r, theta):

        return np.array([
            0.0,
            0.0,
            1 / np.sqrt(self.g_thetatheta(r, theta)),
            0.0
        ])
    
    #validated inside validation/validate_kerr_time_basis.py
    
    def alpha(self, r, theta):
        """
        Lapse function.
        """

        sigma = self.sigma(r, theta)
        delta = self.delta(r)

        A = (
            (r**2 + self.a**2)**2
            - self.a**2 * delta * np.sin(theta)**2
        )

        return np.sqrt(delta * sigma / A)
    
    def e_t(self, r, theta):

        alpha = self.alpha(r, theta)

        omega = (
            -self.g_tphi(r, theta)
            / self.g_phiphi(r, theta)
        )

        return np.array([
            1/alpha,
            0.0,
            0.0,    
            omega/alpha
        ])
    
    #validated inside validation/validate_kerr_tetrad.py
    
    def e_phi(self, r, theta):

        gpp = self.g_phiphi(r, theta)

        return np.array([
            0.0,
            0.0,
            0.0,
            1 / np.sqrt(gpp)
        ])
    
    def basis(self, observer):

        r = observer.radius
        theta = observer.theta

        return {
            "time": self.e_t(r, theta),
            "radial": self.e_r(r, theta),
            "theta": self.e_theta(r, theta),
            "phi": self.e_phi(r, theta)
        }