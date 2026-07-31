import numpy as np


class GaussianBlur:
    """
    Simple 3x3 Gaussian blur.
    """

    def __init__(self):

        self.kernel = np.array(
            [
                [1, 2, 1],
                [2, 4, 2],
                [1, 2, 1]
            ],
            dtype=np.float32
        )

        self.kernel /= np.sum(self.kernel)

    def apply(self, image):

        image = image.astype(np.float32)

        h, w, _ = image.shape

        result = image.copy()

        for y in range(1, h - 1):
            for x in range(1, w - 1):

                patch = image[
                    y-1:y+2,
                    x-1:x+2
                ]

                for c in range(3):

                    result[y, x, c] = np.sum(
                        patch[:, :, c] * self.kernel
                    )

        return result.astype(np.uint8)