import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from rendering.video_encoder import VideoEncoder

encoder = VideoEncoder(
    fps=10
)

encoder.encode()