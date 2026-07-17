import numpy as np

from models.black_hole import BlackHole
from physics.schwarzschild_metric import SchwarzschildMetric
from physics.christoffel_old import ChristoffelSymbols as OldChristoffel
from physics.christoffel import ChristoffelSymbols as NewChristoffel
from physics.schwarzschild_derivatives import SchwarzschildDerivatives

#Create a black hole
bh = BlackHole(mass=1.0)

metric = SchwarzschildMetric(bh)

derivatives = SchwarzschildDerivatives(metric)

old = OldChristoffel(bh)

new = NewChristoffel(metric, derivatives)

gamma_old = old.compute(50, np.pi / 2)

gamma_new = new.compute(50, np.pi / 2)

print("\n=========================")
print("CHRISTOFFEL SYMBOLS")
print("===========================")

for lam in range(4):
    for mu in range(4):
        for nu in range(4):

            if abs(gamma_old[lam,mu,nu]) > 1e-12:

                print(
                    gamma_old[lam,mu,nu],
                    gamma_new[lam, mu, nu]
                )