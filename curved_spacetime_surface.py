import numpy as np
import matplotlib.pyplot as plt

#constants(scaled units)
G = 1  # Gravitational constant
M = 10  # Mass of the central object
c = 1  # Speed of light

#Schwarschild radius
R_s = 2 * G * M / c**2

#Radius coordinates
r = np.linspace(R_s + 0.1, 50, 500)

#Embedding surface (simplified)
z = 2*np.sqrt(R_s * (r - R_s))

#Create circular surface
theta = np.linspace(0, 2 * np.pi, 500)
R, Theta = np.meshgrid(r, theta)

X = R * np.cos(Theta)
Y = R * np.sin(Theta)
Z = 2 * np.sqrt(R_s * (R - R_s))

#Plot
fig = plt.figure(figsize = (10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

ax.set_title('Curved Spacetime Surface around a Mass')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis (Curvature)')
plt.show()