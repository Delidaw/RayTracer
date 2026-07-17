import numpy as np

from physics.ray_generator import RayGenerator
from physics.orbit_simulator import OrbitSimulator
from rendering.star_field import StarField

class SchwarzschildRayTracer:
    """
    Main rendering engine for Schwarzschild spacetime.
    """

    def __init__(
        self,
        black_hole,
        camera
    ):

        self.black_hole = black_hole

        self.camera = camera

        self.simulator = OrbitSimulator(
            black_hole
        )

        self.generator = RayGenerator(
            black_hole
        )

        self.star_field = StarField()

        self.stars = self.star_field.generate()


    def render(self):
        
        image = np.zeros(
            (
                self.camera.height,
                self.camera.width,
                3
            )
        )

        directions = self.camera.ray_directions()

        #loop over every pixel
        for i in range(self.camera.height):

            for j in range(self.camera.width):

                direction = directions[i, j]

                #generate a photon
                state = self.generator.generate(
                    self.camera.observer,
                    direction
                )

                if i == self.camera.height // 2:
                    if j in [0, self.camera.width // 2, self.camera.width - 1]:
                        print(f"\nPixel ({i},{j})")
                        print("Direction:", direction)
                        print("Momentum:", state[4:])  # kt, kr, ktheta, kphi

                #print("\n----- STATE -----")
                #print(type(state))
                #print(state.dtype)
                #print(state)

                result = self.simulator.simulate(
                    state,
                    step_size=0.05,
                    steps=5000
                )

                print("r start:", trajectory[0,1])
                print("r end  :", trajectory[-1,1])
                print("min r  :", np.min(trajectory[:,1]))



                if i == self.camera.height // 2:
                    if j in [0, self.camera.width//2, self.camera.width-1]:

                        print("Pixel", j)
                        print("Captured:", result["captured"])
                        print("Escaped :", result["escaped"])


                #print(type(result))
                #break

                trajectory = result["trajectory"]

                captured = result["captured"]

                escaped = result["escaped"]

                theta = trajectory[-1, 2]
                phi = trajectory[-1, 3]


                trajectory[-1,1]      # final radius
                trajectory[-1,2]      # theta
                trajectory[-1,3]      # phi

                """image[i, j] = self.star_field.sample(
                    theta,
                    phi,
                    self.stars
                )"""
                """
                print ("theta", theta, type(theta))
                print("phi:", phi, type(phi))
                """
                
                """
                print(pixel)
                print([type(x) for x in pixel])

                print("\n----- PIXEL -----")
                print(type(pixel))
                print(pixel)
                """

                if captured:

                    image[i, j] = np.array([
                        0.0,
                        0.0,
                        0.0
                    ])

                else:

                    image[i, j] = self.star_field.sample(
                        theta,
                        phi,
                        self.stars
                    )
        return image
        