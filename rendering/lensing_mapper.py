import numpy as np

"""
class LensingMapper:
    
    Converts an escaping photon trajectory into
    a direction on the celestial sphere.
    

    def direction(self, trajectory):

        state = trajectory[-1]

        direction = state[5:8]

        norm = np.linalg.norm(direction)

        if norm == 0:
            return np.array([0.0, 0.0, 1.0])

        return direction / norm
        """

class LensingMapper:

    def direction(self, trajectory):

        state = trajectory[-1]

        theta = state[2]
        phi   = state[3]

        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)

        return np.array([x, y, z])