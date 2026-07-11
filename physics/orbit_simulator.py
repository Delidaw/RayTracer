import numpy as np

from physics.geodesics import GeodesicEquation
from physics.integrator import RK4Integrator

class OrbitSimulator:
    """
    Simulates particle motion in Schwarzschild spacetime.
    """

    def __init__(self, black_hole):

        self.equation = GeodesicEquation(black_hole)

        self.integrator = RK4Integrator(self.equation)


    def simulate(self, initial_state, step_size, steps):

        """
        Simulate particle motion through Schwarzschild spacetime.

    Parameters
    ----------
    initial_state : ndarray
        Initial state vector.

    step_size : float
        RK4 integration step size.

    steps : int
        Maximum number of integration steps.

    Returns
    -------
    ndarray
        Complete trajectory.
    """
        state = initial_state.copy()

        trajectory = []

        #Schwarzschild radius
        R_s = self.equation.connection.black_hole.schwarzschild_radius

        #Each iteration does 
        # #current state -> 
        # stores it ->
        # advance one rk4 step
        # repeat  

        for _ in range(steps):

            trajectory.append(state.copy())

            state = self.integrator.step(
                state,
                step_size
            )

            #Stop when the particle reaches event horizon
            if state[1] <= R_s:
                print("Particle reached event horizon.")
                trajectory.append(state.copy())
                break 

        return np.array(trajectory)
    
    def orbital_period(self, initial_state):
        """
        Compute the orbital period in proper state
        """

        uphi = initial_state[7]

        if abs(uphi) < 1e-12:
            raise ValueError(
                "Radial trajectories have no orbital period."
            )
        
        return 2 * np.pi / uphi