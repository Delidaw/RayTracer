import numpy as np

from physics.geodesics import GeodesicEquation
from physics.integrator import RK4Integrator
from validation.validate_caustics import trajectory
from physics.adaptive_rk4 import AdaptiveRK4

class OrbitSimulator:
    """
    Simulates particle motion in Schwarzschild spacetime.
    """

    def __init__(self, metric, derivatives):

        self.metric = metric

        self.equation = GeodesicEquation(metric, derivatives)

        self.integrator = RK4Integrator(self.equation)

        self.adaptive = AdaptiveRK4()


    def simulate(self, 
                initial_state, 
                step_size, 
                steps,
                escape_radius = 100
            ):

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

        status = "max_steps"

        #Schwarzschild radius
        #R_s = self.equation.connection.black_hole.schwarzschild_radius

        #event horizon
        R_h = self.metric.event_horizon_radius()

        #Each iteration does 
        # #current state -> 
        # stores it ->
        # advance one rk4 step
        # repeat  

        #print(initial_state)

        for _ in range(steps):

            trajectory.append(state.copy())

            h = self.adaptive.step_size(
                state[1]
            )

            state = self.integrator.step(
                state,
                h
            )

            # --------------------------------------------------
            # Numerical stability check
            # --------------------------------------------------

            if not np.all(np.isfinite(state)):
                status = "numerical_error"

                trajectory.append(state.copy())

                break

#            print(
#                f"step={_}  r={state[1]:.6f}  phi={state[3]:.6f}"
#            )

            #------------------
            # Escape Condition
            #------------------

            r = state[1]
            kr = state[5]

            # Photon has travelled sufficiently far away
            # and is moving outward.

            if r >= escape_radius and kr > 0.0:

                escaped = True
                status = "escaped"

                trajectory.append(state.copy())

                break


            #------------------
            #Event Horizon (capture)
            #------------------
            #Stop when the particle reaches event horizon
            if state[1] <= R_h:
                captured = True
                status = "captured"

                trajectory.append(state.copy())
                break 

        return {
            "trajectory": np.array(trajectory),
            "captured": captured,
            "escaped": escaped,
            "status": status,
            "steps": len(trajectory)
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