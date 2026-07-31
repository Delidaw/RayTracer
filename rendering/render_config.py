class RenderConfig:
    """
    Stores all renderer parameters.
    """

    def __init__(
        self,
        width=800,
        height=800,
        fov=60,
        step_size=0.05,
        steps=300
    ):

        self.width = width
        self.height = height

        self.fov = fov

        self.step_size = step_size
        self.steps = steps