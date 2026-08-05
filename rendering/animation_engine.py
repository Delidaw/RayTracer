import numpy as np

from rendering.frame_exporter import FrameExporter
from rendering.video_encoder import VideoEncoder
from rendering.camera_paths import OrbitPath

class AnimationEngine:
    """
    Controls time-dependent animation of Stella Nova.

    The animation engine updates the observer position
    and asks the existing ray tracer to render each frame.
    """

    def __init__(
        self,
        tracer,
        controller,
        frames=10,
    ):
        self.tracer = tracer
        self.controller = controller
        self.frames = frames

        self.exporter = FrameExporter()
        self.encoder = VideoEncoder()

    def render_frames(self):

        for frame in range(self.frames):

            print()
            print("=" * 50)
            print(
                f"Animation Frame "
                f"{frame + 1}/{self.frames}"
            )
            print("=" * 50)

            self.update(frame)

            image = self.tracer.render()

            self.exporter.save(
                image,
                frame
            )

        print()
        print("Encoding video...")

        self.encoder.encode()

        print()
        print("=" * 50)
        print("Animation Complete")
        print("=" * 50)

    def update(self, frame):
        """
        Move the observer around the black hole.

        The observer completes one full 360-degree orbit
        over the animation.
        """

        observer = self.camera.observer

        observer.phi = (
            2.0 * np.pi *
            frame /
            self.frames
        )

        self.controller.update(
            frame,
            self.frames
        )