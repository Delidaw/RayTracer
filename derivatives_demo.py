import numpy as np

from models.black_hole import BlackHole
from physics.schwarzschild_metric import SchwarzschildMetric
from physics.schwarzschild_derivatives import SchwarzschildDerivatives

# Create black hole
bh = BlackHole(mass=1.0)

# Create metric
metric = SchwarzschildMetric(bh)

# Create derivative calculator
derivatives = SchwarzschildDerivatives(metric)

# Compute derivatives
dg = derivatives.compute(
    r=50,
    theta=np.pi/2
)

coords = ["t", "r", "θ", "φ"]

print("\n====================")
print("METRIC DERIVATIVES")
print("====================")

for alpha in range(4):
    for mu in range(4):
        for nu in range(4):

            value = dg[alpha, mu, nu]

            if abs(value) > 1e-12:
                print(
                    f"∂g[{coords[mu]},{coords[nu]}]/∂{coords[alpha]}"
                    f" = {value:.6f}"
                )