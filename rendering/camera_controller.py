class CameraController:
    """
    Controls camera motion.

    The controller owns a camera and delegates
    movement to a selected CameraPath.
    """

    def __init__(
        self,
        camera,
        path
    ):
        self.camera = camera
        self.path = path

    @property
    def observer(self):
        return self.camera.observer

    def update(
        self,
        frame,
        total_frames
    ):
        self.path.update(
            self.observer,
            frame,
            total_frames
        )