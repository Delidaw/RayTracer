import numpy as np

class ParticleEnsemble:
    """
    Simulates multiple particles in schwarzschild spacetime.
    """

    #why not ParticleEnsemble(black_hole) 
    #why ParticleEnsemble(simulator)
    """
    because we don't want the ensemble to know 
    what is happening in geodesic. 
    Its job is simply:

"Here are particles. Ask the simulator to evolve them."

That's called separation of responsibilities."""

    def __init__(self, simulator):

        self.simulator = simulator
        self.particles = []

    def add_particle(self, name, state):

        """
        Add one particle to the ensemble.
        """

        self.particles.append({
            "name": name,
            "state": state
        })

    def clear(self):
        """
        Remove all particles.
        """

        self.particles.clear()

    def simulate_all(self, step_size, steps):
        """
        Simulate every particle in the ensemble.
        Returns
        -------
        list
        List of trajectories, one per particle.
        """

        trajectories = []

        for particle in self.particles:
            trajectory = self.simulator.simulate(
                particle["state"],
                step_size,
                steps
            )

            trajectories.append({
                "name": particle["name"],
                "trajectory": trajectory
            })  

        return trajectories