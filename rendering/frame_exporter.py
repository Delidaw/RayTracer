import os

import matplotlib.pyplot as plt


class FrameExporter:
    """
    Saves rendered frames to disk.

    These frames can later be combined into
    GIFs or MP4 videos.
    """

    def __init__(
        self,
        output_directory="frames"
    ):

        self.output_directory = output_directory

        os.makedirs(
            output_directory,
            exist_ok=True
        )

    def save(
        self,
        image,
        frame_number
    ):

        filename = os.path.join(
            self.output_directory,
            f"frame{frame_number:04d}.png"
        )

        plt.imsave(
            filename,
            image
        )

        print(
            f"Saved {filename}"
        )