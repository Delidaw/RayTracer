import numpy as np

from physics.geodesics import GeodesicEquation
from physics.integrator import RK4Integrator

class OrbitSimulator:
    """
    Simulates particle motion in Schwarzschild spacetime.
    """

    def __init__(self, metric, derivatives):

        self.metric = metric

        self.equation = GeodesicEquation(metric, derivatives)

        self.integrator = RK4Integrator(self.equation)


    def simulate(self, initial_state, step_size, steps):

        """
        Simulate particle motion in an arbitrary spacetime.

        because now it can simulate:

        Schwarzschild spacertime
        Kerr spacertime
        Reissner–Nordström (future) spacetime
        Kerr–Newman (future) spacetime

without modification.

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

        captured = False
        escaped = False

        #Schwarzschild radius
        #R_s = self.equation.connection.black_hole.schwarzschild_radius

        #event horizon
        R_h = self.metric.event_horizon_radius()

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

            #------------------
            #Escape Condition
            #------------------
            if state[1] > 100:
                escaped = True
                trajectory.append(state.copy())
                break


            #------------------
            #Event Horizon (capture)
            #------------------
            #Stop when the particle reaches event horizon
            if state[1] <= R_h:
                captured = True
                trajectory.append(state.copy())
                break 

        return {
            "trajectory": np.array(trajectory),
            "captured": captured,
            "escaped": escaped
}
    
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