"""
dg[0] = ∂g/∂t      = all zeros

dg[1] = ∂g/∂r
         dg[1,0,0] = -R_s/r²
         dg[1,1,1] = -R_s/(r-R_s)²
         dg[1,2,2] = 2r
         dg[1,3,3] = 2r sin²θ

dg[2] = ∂g/∂θ
         dg[2,3,3] = 2r² sinθ cosθ

dg[3] = ∂g/∂φ      = all zeros
"""

from abc import ABC, abstractmethod

class MetricDerivatives(ABC):

    """
    Abstract base class for metric derivatives.
    
    Computes 
    ∂g_{μν} / ∂x^α

    Returns
    -------
    dg : numpy.ndarray
        Shape (4, 4, 4)

        dg[0] = ∂g/∂t
        dg[1] = ∂g/∂r
        dg[2] = ∂g/∂θ
        dg[3] = ∂g/∂φ
    """

    @abstractmethod
    def compute(self, r, theta):
        """
        Returns 
        dg[α, μ, ν]

        Shape

            (4,4,4)
        """
        pass