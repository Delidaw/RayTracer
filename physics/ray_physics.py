import numpy as np

class RayPhysics:

    """
    Collection of physical calculations used 
    during Schwarzschild ray tracing.
    """

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def redshift(self, radius):
        """
        Gravitational redshift factor.

    Returns

        ν_observed / ν_emitted (fo / fe)
        """

        R_s = self.black_hole.schwarzschild_radius

        if radius <= R_s:
            return 0.0
        
        return np.sqrt( 1 - R_s / radius)
    

    def escape_velocity(self, radius):

        """
        Escape velocity in schwarzschild units.
        """

        R_s = self.black_hole.schwarzschild_radius

        return np.sqrt(R_s / radius)
    
    def orbital_velocity(self, radius):

        """
        Circular orbital velocity.
        """

        R_s = self.black_hole.schwarzschild_radius

        return np.sqrt(
            R_s / 
            (2 * (radius - R_s))
        )
    
    def lensing_strength(self, radius):

        """
        Simple measure of gravitational lensing strength.
        """

        R_s = self.black_hole.schwarzschild_radius

        return R_s / radius