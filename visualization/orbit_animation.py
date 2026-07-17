import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class OrbitAnimation:

    def __init__(self):
        pass

    def spherical_to_cartesian(self, trajectory):

        r = trajectory[:,1]
        theta = trajectory[:,2]
        phi = trajectory[:,3]

        x = r*np.sin(theta)*np.cos(phi)
        y = r*np.sin(theta)*np.sin(phi)
        z = r*np.cos(theta)

        return x, y, z
    
    def animate(self, trajectory):

        x, y, z = self.spherical_to_cartesian(
            trajectory
        )

        fig, ax = plt.subplots(figsize=(7,7))

        ax.set_aspect("equal")

        ax.grid(True)

        ax.set_xlabel("x")

        ax.set_ylabel("y")

        ax.set_title("Orbit Animation")

        ax.scatter(
            0,
            0,
            s=500,
            color="black",
            label="Black Hole"
        )

        trail, = ax.plot(
            [],
            [],
            lw=2
        )

        particle, = ax.plot(
            [],
            [],
            "ro",
            markersize=6
        )

        margin = 2

        ax.set_xlim(
            np.min(x)-margin,
            np.max(x)+margin
        )

        ax.set_ylim(
            np.min(y)-margin,
            np.max(y)+margin
        )

        def init():

            trail.set_data([], [])

            particle.set_data([], [])

            return trail, particle
        
        def update(frame):

            trail.set_data(
                x[:frame],
                y[:frame]
            )

            particle.set_data(
                [x[frame]],
                [y[frame]]
            )

            return trail, particle
        
        animation = FuncAnimation(

        fig,

        update,

        frames=len(x),

        init_func=init,

        interval=20,

        blit=True
        )

        plt.show()