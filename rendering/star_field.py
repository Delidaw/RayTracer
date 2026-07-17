import numpy as np

class StarField:
    """
    Represents the celestial sphere surrounding
    the black hole.
    """

    def __init__(self, seed=42):

        self.rng = np.random.default_rng(seed)

    #generating stars
    def generate(
        self,
        n_stars=50000
    ):
        theta = self.rng.uniform(
            0,
            np.pi, 
            n_stars
        )

        phi = self.rng.uniform(
            0, 
            2 * np.pi,
            n_stars
        )

        brightness = self.rng.uniform(
            0.4,
            1.0,
            n_stars
        )

        # Stellar temperatures (Kelvin)
        temperature = self.rng.uniform(
            3000,
            12000,
            n_stars
        )

        colors = np.array([
            self.temperature_to_rgb(T)
            for T in temperature
        ])

        return {

            "theta": theta,

            "phi": phi,

            "brightness": brightness,

            "temperature": temperature,

            "color": colors

        }
    
    def temperature_to_rgb(self, T):

        """
    Approximate stellar color from temperature.

    Parameters
    ----------
    T : float
        Temperature in Kelvin.

    Returns
    -------
    ndarray
        RGB values in [0,1].
    """
        
        if T < 4000:
            return np.array([1.0, 0.55, 0.30]) #-->red
        
        elif T < 5500:
            return np.array([1.0, 0.90, 0.70]) #-->orange
        
        elif T < 7000:
            return np.array([1.0, 1.0, 1.0]) #--> white
        
        elif T < 9000:
            return np.array([0.75, 0.85, 1.0])  #--> cyan
        
        else:
            return np.array([0.55, 0.70, 1.0]) #--> dark blue
        
    def sample(
        self,
        theta,
        phi,
        stars
    ):
        """
        Returns the color of the nearest star
        in the given direction.
        """

        dtheta = stars["theta"] - theta
        dphi = stars["phi"] - phi

        #aprroximating angular distance
        distance = np.sqrt(
            dtheta **2 + 
            dphi **2
        )

        #finding the closest star
        nearest = np.argmin(distance)

        #visibility threshold
        threshold = 0.06

        if distance[nearest] < threshold:
            return(
                stars["color"][nearest]
                * stars["brightness"][nearest]
            )
        
        return np.array([0.0, 0.0, 0.0])