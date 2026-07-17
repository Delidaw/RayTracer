import numpy as np


class Camera:
    """
    Represents a pinhole camera used for ray tracing.

    The camera defines the image resolution and
    field of view, but it is independent of any
    particular spacetime.
    """

    def __init__(
        self,
        width,
        height,
        fov=60.0
    ):
        self.width = width
        self.height = height
        self.fov = fov

    @property
    def aspect_ratio(self):
        """
        Width divided by height.
        """
        return self.width / self.height