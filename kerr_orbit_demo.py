import numpy as np

from models.black_hole import BlackHole
from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.orbit_simulator import OrbitSimulator

bh = BlackHole(
    mass = 1.0,
    spin = 0.5
)

metric = KerrMetric(bh)

derivatives = KerrDerivatives(metric)

simulator = OrbitSimulator(
    metric, 
    derivatives
)

state = np.array([
    0.0,          # t
    10.0,         # r
    np.pi/2,      # theta
    0.0,          # phi

    1.0,          # ut
    0.0,          # ur
    0.0,          # utheta
    0.05          # uphi
])

result = simulator.simulate(
    initial_state=state,
    step_size=0.01,
    steps=500
)

trajectory = result["trajectory"]

print("\n====================")
print("KERR ORBIT")
print("====================")

print("Captured : ", result["captured"])
print("Escaped : ", result["escaped"])
print("Steps : ", len(trajectory))

print("\nInitial State")
print(trajectory[0])

print("\nFinal state: ")
print(trajectory[-1])