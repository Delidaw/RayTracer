class ParticleEnsemble:
    """
    Simulates multiple particles using an OrbitSimulator.
    """

    def __init__(self, simulator):

        self.simulator = simulator
        self.particles = []


    def add_particle(self, name, state):

        self.particles.append({
            "name": name,
            "state": state
        })


    def clear(self):

        self.particles.clear()


    def simulate_all(self, step_size, steps):

        trajectories = []

        for particle in self.particles:

            simulation = self.simulator.simulate(
                particle["state"],
                step_size,
                steps
            )

            trajectories.append({
                "name": particle["name"],
                "trajectory": simulation["trajectory"],
                "status": simulation["status"],
                "captured": simulation["captured"],
                "escaped": simulation["escaped"],
                "steps": simulation["steps"]
            })

        return trajectories