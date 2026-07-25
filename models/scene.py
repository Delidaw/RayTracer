class Scene:
    """
    Represents everything that exists in the universe.
    
    The ray tracer asks the scene 
    what a photon encounters.
    """

    def __init__(
            self,
            black_hole,
            observer,
            star_field = None,
            accretion_disk = None
    ):
        self.black_hole = black_hole
        self.observer = observer

        self.star_field = star_field
        self.accretion_disk = accretion_disk