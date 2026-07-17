import numpy as np


class ImagePlane:
    """
    Represents the physical image plane
    located one unit in front of the camera.
    """

    def __init__(self, camera):

        """
        Instead of storing
        self.width and self.height
        we compute them whenever they're requested.
        That means if later you do
        camera.fov = 90
        the image plane automatically updates.
        No synchronization bugs.
        """
 
        self.camera = camera

        self.distance = 1.0

    @property
    def height(self):
        """
        Physical height of the image plane.
        """

        fov = np.deg2rad(self.camera.fov)

        return 2 * self.distance * np.tan(fov / 2)

    @property
    def width(self):
        """
        Physical width of the image plane.
        """

        return self.camera.aspect_ratio * self.height