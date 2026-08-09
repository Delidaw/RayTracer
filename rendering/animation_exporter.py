import imageio.v2 as imageio
import numpy as np


class AnimationExporter:
    """
    Exports rendered Photon Forge animation frames
    to GIF and MP4 formats.
    """

    def __init__(self, fps=10):
        self.fps = fps

    # ==================================================
    # GIF
    # ==================================================

    def save_gif(self, frames, filename):
        """
        Save rendered frames as an animated GIF.
        """

        print()
        print("=" * 60)
        print("Animation Export")
        print("=" * 60)

        imageio.mimsave(
            filename,
            [
                np.clip(
                    frame,
                    0,
                    255
                ).astype(np.uint8)
                for frame in frames
            ],
            fps=self.fps
        )

        print("Format : GIF")
        print(f"Frames : {len(frames)}")
        print(f"FPS    : {self.fps}")
        print(f"Output : {filename}")
        print("=" * 60)

    # ==================================================
    # MP4
    # ==================================================

    def save_mp4(self, frames, filename):
        """
        Save rendered frames as an MP4 video.

        Uses imageio's ffmpeg backend.
        """

        print()
        print("=" * 60)
        print("Animation Export")
        print("=" * 60)

        writer = imageio.get_writer(
            filename,
            fps=self.fps,
            format="FFMPEG",
            codec="libx264",
            quality=8
        )

        try:

            for frame in frames:

                frame_uint8 = np.clip(
                    frame,
                    0,
                    255
                ).astype(np.uint8)

                writer.append_data(frame_uint8)

        finally:

            writer.close()

        print("Format : MP4")
        print(f"Frames : {len(frames)}")
        print(f"FPS    : {self.fps}")
        print(f"Output : {filename}")
        print("=" * 60)