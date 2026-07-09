import numpy as np

from models.black_hole import BlackHole
from physics.christoffel import ChristoffelSymbols

#Create a black hole
bh = BlackHole(mass = 10)

#Create a christoffel symbols calculator
christoffel = ChristoffelSymbols(bh)

#Create Christoffel tensor
gamma = christoffel.compute(r = 50, theta = np.pi / 2)

labels = ["t", "r", "θ", "φ"]

print("\n=========================")
print("CHRISTOFFEL SYMBOLS")
print("===========================")

for lam in range(4):
    for mu in range(4):
        for nu in range(4):
            value = gamma[lam, mu, nu]

            if abs(value) > 1e-12:
                print(
                    f"Γ^{labels[lam]}_{{{labels[mu]}{labels[nu]}}}"
                    f" = {value:.6f}"
                )