import numpy as np


class Bloom:
    """
    Applies a simple bloom effect
    to bright pixels.
    """

    def __init__(
        self,
        threshold=180,
        strength=0.35
    ):

        self.threshold = threshold
        self.strength = strength

    def apply(
        self,
        image
    ):

        bloom = image.astype(np.float32).copy()

        brightness = np.mean(
            bloom,
            axis=2
        )

        mask = brightness > self.threshold

        glow = np.zeros_like(bloom)

        glow[mask] = bloom[mask]

        bloom = bloom + self.strength * glow

        bloom = np.clip(
            bloom,
            0,
            255
        )

        return bloom.astype(np.uint8)