import numpy as np


class CameraPath:
    """
    Base class for all camera motions.
    """

    def update(
        self,
        observer,
        frame,
        total_frames
    ):
        raise NotImplementedError

class OrbitPath(CameraPath):
    """
    Camera performs one complete orbit
    around the black hole.
    """

    def update(
        self,
        observer,
        frame,
        total_frames
    ):

        observer.phi = (
            2.0
            * np.pi
            * frame
            / total_frames
        )

class ZoomPath(CameraPath):
    """
    Camera moves radially
    toward the black hole.
    """

    def __init__(
        self,
        start_radius=20,
        end_radius=6
    ):

        self.start_radius = start_radius
        self.end_radius = end_radius

    def update(
        self,
        observer,
        frame,
        total_frames
    ):

        t = frame / (total_frames - 1)

        observer.radius = (
            self.start_radius
            +
            t *
            (
                self.end_radius
                - self.start_radius
            )
        )

class SpiralPath(CameraPath):
    """
    Orbit while simultaneously
    moving inward.
    """

    def __init__(
        self,
        start_radius=20,
        end_radius=6
    ):

        self.start_radius = start_radius
        self.end_radius = end_radius

    def update(
        self,
        observer,
        frame,
        total_frames
    ):

        t = frame / (total_frames - 1)

        observer.radius = (
            self.start_radius
            +
            t *
            (
                self.end_radius
                - self.start_radius
            )
        )

        observer.phi = (
            4.0
            * np.pi
            * t
        )