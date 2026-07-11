import numpy as np

class PhotonInitialConditions:
    """
    Generates physically consistent initial
    conditions for photons in schwarzschild spacetime.
    """

    def __init__(self, black_hole):

        self.black_hole = black_hole

    def _build_state(self, radius, kt, kr, kphi):
        """
        Construct the photon state vector
        confined to the equatorial plane.
        """

        return np.array([
            0.0,          # t
            radius,       # r
            np.pi / 2,    # theta
            0.0,          # phi

            kt,   #wave vectors not velocities
            kr,
            0.0,          # k_theta
            kphi
        ])
    
    def radial_ray(self, radius, inward = True):
        """
    Initial conditions for a purely radial photon.
    """
        
        R_s = self.black_hole.schwarzschild_radius

        if radius <= R_s:
            raise ValueError(
                "Photon must start outside the event Horizon."
            )
        
        f = 1 - R_s / radius
        kt  = 1.0

        if inward: 
            kr = -f

        else:
            kr = f

        return self._build_state(
            radius,
            kt, kr,
            0.0
        )


    def light_ray(self, radius, impact_parameter):
        """
    Photon launched toward the black hole
    with a specified impact parameter(b).
    """
        R_s = self.black_hole.schwarzschild_radius

        if radius <= R_s:
            raise ValueError(
                "Photon must start outside the event horizon."
            )

        f = 1 - R_s / radius

        kt = 1.0

        kphi = impact_parameter / radius**2
    
        radicand = f * (
            f * kt**2
            - radius**2 * kphi**2
        )

        if radicand < 0:
            raise ValueError(
                "Impact parameter is too large for this starting radius."
            )
        kr = -np.sqrt(radicand)

        return self._build_state(
            radius,
            kt,
            kr,
            kphi
        )