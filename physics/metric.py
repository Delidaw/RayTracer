from abc import ABC, abstractmethod
import numpy as np

#KERR METRIC

class Metric(ABC):
    """
    Abstract base class for spacetime metrics.
    Every metric must implement these methods.
    """

    def __init__(self, M = 1.0):
        """
        Abstract base class for spacetime metrics.
        Every metric must implement these methods.
        """
        self.M = M

    @abstractmethod
    def metric_tensor(self, coords):
        """
        Returns g_{μν}
            Parameters
            ----------
            coords : array-like
                (t, r, theta, phi)

            Returns
            -------
            numpy.ndarray
            4x4 metric tensor
            """
        pass

    @abstractmethod
    def inverse_metric(self, coords):
        """
            Returns g^{μν}
            """
        pass

    @abstractmethod
    def event_horizon_radius(self):
        """
            Radius of the event horizon.
            """
        pass
    
