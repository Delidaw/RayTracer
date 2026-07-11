import numpy as np

class InitialConditions:

    """
    Generates physically consistent initial states
    for particle and photons in Schwarzschild spacetime
    """

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def compute_ut(self, radius, ur, uphi):
        """
        Compute the time component of the four velocity
        from the normalization condition
        
            g_{μν}u^μu^ν = -1
        for a massive particle in Schwarzschild spacetime.
        """

        R_s = self.black_hole.schwarzschild_radius

        f = 1 - R_s / radius
        if f <= 0:
            raise ValueError(
                "Initial radius must be outside the vent horizon."
            )
        
        ut = np.sqrt(
            (
                1 
                + (ur ** 2) / f
                + radius  ** 2 * uphi **2 
            ) / f
        )

        return ut

    def radial_infall(self, radius):

        R_s = self.black_hole.schwarzschild_radius

        if radius <= R_s:
            raise ValueError(
                "Particle must start outside the event horizon."
            )

        ut = 1.0 / np.sqrt(1 - R_s / radius)

        return np.array([
            0.0,
            radius,
            np.pi / 2,
            0.0,

            ut,
            0.0,
            0.0,
            0.0
        ])
    
    def circular_orbit(self, radius):

        R_s = self.black_hole.schwarzschild_radius

        mass_parameter = R_s / 2

        if radius <= 3 * mass_parameter:
            raise ValueError(
                "Stable circular orbits require radius > 6M (3 * Schwarzschild radius)."
            )

        omega = np.sqrt(mass_parameter / radius**3)

        ut = 1 / np.sqrt(1 - 3 * mass_parameter / radius)

        uphi = omega * ut

        return self._build_state(
            radius,
            ut,
            0.0,
            uphi
        )
    
    def escape_trajectory(self, radius, radial_velocity, angular_velocity = 0.0):
        """
        Initial conditions for escaping particle.

    Parameters
    ----------
    radius : float
        Initial radius.

    radial_velocity : float
        Initial outward radial velocity (u^r > 0).

    angular_velocity : float, optional
        Initial angular component (u^φ).
        """

        ut = self.compute_ut(
            radius, 
            radial_velocity,
            angular_velocity
        )

        return self._build_state(
            radius, 
            ut, radial_velocity,
            angular_velocity
        )
    
    def elliptical_orbit(self, semi_major_axis, eccentricity):

        if semi_major_axis <= 0:
            raise ValueError("Semi-major axis must be positive.")

        if not (0 <= eccentricity < 1):
            raise ValueError("Eccentricity must satisfy 0 <= e < 1.")

        mass_parameter = self.black_hole.schwarzschild_radius / 2

        r_peri = semi_major_axis * ( 1 - eccentricity)

        v_peri = np.sqrt(
            mass_parameter * 
            (
                2 / r_peri
                - 1 / semi_major_axis
            )
        )

        uphi = v_peri / r_peri

        ut = self.compute_ut(
            r_peri,
            0.0,
            uphi
        )

        return self._build_state(
            r_peri,
            ut,
            0.0,
            uphi
        )
    
    def _build_state(self, radius, ut, ur, uphi):
        """
        Construct the state vector for a particle
        confined to the the equitorial plane.
        """

        return np.array([
            0.0,           # t
        radius,        # r
        np.pi / 2,     # theta
        0.0,           # phi

        ut,
        ur,
        0.0,           # u_theta
        uphi
        ])
    