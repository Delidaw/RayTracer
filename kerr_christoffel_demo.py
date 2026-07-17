import numpy as np

from models.black_hole import BlackHole

from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.christoffel import ChristoffelSymbols

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

gamma = christoffel.compute(
    10,
    np.pi/2
)

print("\n==============================")
print("KERR CHRISTOFFEL SYMBOLS")
print("==============================")

for lam in range(4):
    for mu in range(4):
        for nu in range(4):

            if abs(gamma[lam, mu, nu]) > 1e-12:

                print(
                    f"Γ^{lam}_{mu}{nu} = "
                    f"{gamma[lam,mu,nu]:.8f}"
                )