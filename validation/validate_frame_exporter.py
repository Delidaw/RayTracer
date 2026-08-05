import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import numpy as np

from rendering.frame_exporter import FrameExporter


exporter = FrameExporter()

image = np.random.rand(
    100,
    100,
    3
)

exporter.save(
    image,
    0
)

print()
print("=" * 60)
print("FRAME EXPORTER VALIDATION COMPLETE")
print("=" * 60)