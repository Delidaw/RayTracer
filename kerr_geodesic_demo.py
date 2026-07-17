import numpy as np

from models.black_hole import BlackHole

from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.christoffel import ChristoffelSymbols
from physics.geodesics import GeodesicEquation

bh = BlackHole(
    mass=1.0,
    spin=0.5
)

metric = KerrMetric(bh)

derivatives = KerrDerivatives(metric)

christoffel = ChristoffelSymbols(
    metric,
    derivatives
)

equation = GeodesicEquation(metric, derivatives)

state = np.array([
    0.0,          # t
    10.0,         # r
    np.pi/2,      # theta
    0.0,          # phi

    1.0,          # u^t
    0.0,          # u^r
    0.0,          # u^theta
    0.05          # u^phi
])

dstate = equation.derivatives(state)

print("\n==========================")
print("STATE DERIVATIVES")
print("==========================")

print(dstate)