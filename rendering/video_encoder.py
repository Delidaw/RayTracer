import os
import imageio.v2 as imageio


class VideoEncoder:
    """
    Combines exported frames into a video.
    """

    def __init__(
        self,
        frames_directory="frames",
        output_file="black_hole.mp4",
        fps=30,
    ):

        self.frames_directory = frames_directory
        self.output_file = output_file
        self.fps = fps

    def encode(self):

        frames = sorted(

            file

            for file in os.listdir(self.frames_directory)

            if file.endswith(".png")

        )

        if len(frames) == 0:

            raise RuntimeError(
                "No frames found."
            )

        writer = imageio.get_writer(

            self.output_file,

            fps=self.fps

        )

        for frame in frames:

            image = imageio.imread(

                os.path.join(
                    self.frames_directory,
                    frame
                )
            )

            writer.append_data(image)

        writer.close()

        print()
        print("=" * 60)
        print("VIDEO CREATED")
        print("=" * 60)
        print(self.output_file)