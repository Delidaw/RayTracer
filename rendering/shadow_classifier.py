class ShadowClassifier:
    """
    Determines whether a photon belongs
    to the black hole shadow.
    """

    def __init__(self):
        pass

    def is_shadow(self, result):
        """
        Returns True if the photon
        was captured by the black hole.
        """

        return result["captured"]