import numpy as np


class BackgroundSampler:

    def __init__(self, star_field):
        self.star_field = star_field

    def sample(self, state):

        direction = state[5:8]

        direction /= np.linalg.norm(direction)

        return self.star_field.sample(direction)