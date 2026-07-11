# ===============================
# Schwarzschild Black Hole Model
# Phase 1: Physical Properties
# ===============================


import numpy as np

#Constants (scaled units)
G = 1.0  # Gravitational constant
M = 10.0  # Mass of the black hole
c = 1.0  # Speed of light

# Schwarzschild Radius (Event Horizon)
R_s = 2 * G * M / c**2

# Photon Sphere Radius
R_ph = 1.5 * R_s

# Innermost stable circular orbit (ISCO) radius
R_isco = 3 * R_s

# Escape velocity at the Schwarzschild radius
v_esc = np.sqrt(2 * G * M / R_s)


"""
#Radius coordinates
r = np.linspace(R_s + 0.1, 50, 500)

#Embedding surface (simplified)
z = 2*np.sqrt(R_s * (r - R_s))

#Create circular surface
theta = np.linspace(0, 2 * np.pi, 500)
R, Theta = np.meshgrid(r, theta)


"""


print("\n======================================")
print("      SCHWARZSCHILD BLACK HOLE")
print("======================================")
print(f"Mass                     : {M:.2f}")
print(f"Gravitational Constant   : {G:.2f}")
print(f"Speed of Light           : {c:.2f}")
print("--------------------------------------")
print(f"Schwarzschild Radius     : {R_s:.3f}")
print(f"Photon Sphere Radius     : {R_ph:.3f}")
print(f"ISCO Radius              : {R_isco:.3f}")
print(f"Escape Velocity          : {v_esc:.3f}")
print("======================================")