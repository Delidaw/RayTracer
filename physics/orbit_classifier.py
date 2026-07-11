import numpy as np

class OrbitClassifier: 
    """
    Classifies trajectories produced by OrbitSimulator.
    """

    def __init__(self, black_hole):
        self.black_hole = black_hole

    def classify(self, trajectory):
        
        r = trajectory[:, 1]

        R_s = self.black_hole.schwarzschild_radius

        r_initial = r[0]

        r_final = r[-1]

        r_min = r.min()

        r_max = r.max()

        if r_min <= R_s :
            return{
                "classification": "Captured",
                "r_initial": r_initial,
                "r_final": r_final,
                "r_min": r_min,
                "r_max": r_max
            }
        
        if r_final > 2 * r_initial:
            return {
                "classification": "Escape",
                "r_initial": r_initial,
                "r_final": r_final,
                "r_min": r_min,
                "r_max": r_max
            }
        
        return {
            "classification": "Bound Orbit",
            "r_initial": r_initial,
            "r_final": r_final,
            "r_min": r_min,
            "r_max": r_max
        }