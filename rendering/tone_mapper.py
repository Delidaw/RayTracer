import numpy as np


class ToneMapper:
    """
    Converts HDR colours into displayable RGB values.
    """

    def __init__(self, exposure=1.0):
        self.exposure = exposure

    def map(self, hdr_image):
        """
        Applies Reinhard tone mapping.
        """

        image = hdr_image.astype(np.float32)

        image *= self.exposure

        image = image / (1.0 + image)

        image *= 255.0

        image = np.clip(
            image,
            0,
            255
        )

        return image.astype(np.uint8)