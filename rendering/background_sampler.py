import numpy as np

class BackgroundSampler:
    """
    Samples the distant star field.
    """

    def __init__(self, star_field):
        self.star_field = star_field

    def sample(self, state):
        """
        Returns the background brightness.
        
        Parameters
        -----------
        state: ndarray
        Photon state.
        """

        direction = state[5:8]

        norm = np.linalg.norm(direction)

        if norm != 0:
            direction = direction / norm

        value = self.star_field.sample(direction)

        return np.array(
            [
                value,
                value,
                value
            ],
            dtype=np.uint8
        )