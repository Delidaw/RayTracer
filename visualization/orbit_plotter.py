import numpy as np
import matplotlib.pyplot as plt

class OrbitPlotter:

    def __init__(self):
        pass

    def spherical_to_cartesian(self, trajectory):

        r = trajectory[:, 1]
        theta = trajectory[:, 2]
        phi = trajectory[:, 3]

        x = r * np.sin(theta) * np.cos(phi)

        y = r * np.sin(theta) * np.sin(phi)

        z = r * np.cos(theta)

        return x, y, z
    
    def plot(self, trajectory):

        x, y, z = self.spherical_to_cartesian(
            trajectory
        )

        plt.figure(figsize=(7,7))

        plt.plot(
            x,
            y,
            linewidth=2
        )

        plt.scatter(
            0,
            0,
            s=500,
            color="black",
            edgecolors="gold",
            linewidths=2,
            label="Black Hole"
        ) 

        plt.xlabel("x")

        plt.ylabel("y")

        plt.title("Particle Orbit")

        plt.axis("equal")

        plt.grid(True)

        plt.legend()

        plt.show()