import numpy as np


class AnimationEngine:
    """
    Controls time-dependent animation of Stella Nova.

    The animation engine updates the observer position
    and asks the existing ray tracer to render each frame.
    """

    def __init__(
        self,
        tracer,
        camera,
        frames=10
    ):
        self.tracer = tracer
        self.camera = camera
        self.frames = frames

    def render_frames(self):

        rendered_frames = []

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

            rendered_frames.append(image)

        return rendered_frames

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