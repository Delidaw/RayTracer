import numpy as np

from models.black_hole import BlackHole
from physics.schwarzschild_metric import SchwarzschildMetric
bh = BlackHole(mass = 10)

metric = SchwarzschildMetric(bh)

r = 50
theta = np.pi / 2

g = metric.metric_tensor(r, theta)

print("\n====================================")
print("SCHWARZSCHILD METRIC TENSOR")
print("====================================")
print(f"Radius (r) : {r}")
print(f"Theta      : {theta:.3f} rad\n")

print(g)

print("\nIndividual Components")
print(f"g_tt      = {g[0,0]:.6f}")
print(f"g_rr      = {g[1,1]:.6f}")
print(f"g_thetaθ  = {g[2,2]:.6f}")
print(f"g_phiφ    = {g[3,3]:.6f}")