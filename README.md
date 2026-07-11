# RayTracer




<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stella Nova Inspired Black Hole Simulatiion</title>
    <style>
        body, html { 
            margin: 0; 
            padding: 0; 
            overflow: hidden; 
            background-color: #000; 
            width: 100%; 
            height: 100%;
            font-family: monospace;
        }
        canvas { display: block; }
        #ui-overlay {
            position: absolute;
            top: 20px;
            left: 20px;
            color: #00ffcc;
            text-shadow: 0 0 5px rgba(0,255,204,0.5);
            pointer-events: none;
            font-size: 12px;
            letter-spacing: 1px;
            line-height: 1.5;
        }
    </style>
</head>
<body>

    <div id="ui-overlay">
        SYS // GRAVITY_SIM_ACTIVE<br>
        SCHWARZSCHILD RADIUS: 3.0 units<br>
        INTERACTION: CLICK & DRAG TO ROTATE CAMERA
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <script>
        // --- 1. Scene & Renderer Initialization ---
        const scene = new THREE.Scene();
        const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap at 2 for performance
        document.body.appendChild(renderer.domElement);

        // --- 2. Interactive Uniform Trackers ---
        const uniforms = {
            u_resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
            u_time: { value: 0 },
            u_mouse: { value: new THREE.Vector2(0.0, 0.2) } // Initial tilt orientation
        };

        // Target smooth mouse interpolation values
        let targetMouseX = 0.0;
        let targetMouseY = 0.2;
        let isDragging = false;
        let previousMousePosition = { x: 0, y: 0 };

        // --- 3. Shaders Engine (GLSL) ---
        const vertexShader = `
            void main() {
                gl_Position = vec4(position, 1.0);
            }
        `;

        const fragmentShader = `
            uniform vec2 u_resolution;
            uniform vec2 u_mouse;
            uniform float u_time;

            // Simple deterministic pseudo-random hash for stars & dust texture
            float hash(vec3 p) {
                p = fract(p * vec3(443.8975, 397.2973, 491.1871));
                p += dot(p.xyz, p.yzx + 19.19);
                return fract(p.x * p.y * p.z);
            }

            // High-frequency star field using directional vector mapping
            vec3 getBackgroundStars(vec3 rd) {
                float n = hash(floor(rd * 350.0));
                if (n > 0.994) {
                    float intensity = hash(floor(rd * 350.0) + 13.0);
                    return vec3(0.6 + 0.4 * intensity) * smoothstep(0.994, 0.999, n);
                }
                return vec3(0.0);
            }

            void main() {
                // Normalize screen coordinates Aspect Ratio aware (-1 to 1 range)
                vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution.xy) / u_resolution.y;
                
                // Rotational Camera angles based on smooth mouse values
                float angleX = u_mouse.x * 3.14159 * 2.0;
                float angleY = u_mouse.y * 3.14159 * 0.5;
                
                // Camera Placement (Ray Origin) orbiting the singularity
                float camRadius = 14.0;
                vec3 ro = vec3(camRadius * sin(angleX) * cos(angleY), camRadius * sin(angleY), camRadius * cos(angleX) * cos(angleY));
                vec3 target = vec3(0.0, 0.0, 0.0);
                
                // Build Looking-At / Camera Transform Matrix 
                vec3 ww = normalize(target - ro);
                vec3 uu = normalize(cross(ww, vec3(0.0, 1.0, 0.0)));
                vec3 vv = normalize(cross(uu, ww));
                
                // Generate pristine initial Photon Direction ray
                vec3 rd = normalize(uv.x * uu + uv.y * vv + 1.8 * ww);

                // Simulation Config Parameters
                vec3 p = ro;             // Step positions
                vec3 v = rd;             // Current photon velocity component
                float dt = 0.05;         // Step resolution Delta Time

                float GM = 1.5;          // Gravitational Constant * Mass
                float rs = 2.0 * GM;     // Event Horizon (Schwarzschild Radius = 3.0)
                
                vec3 finalColor = vec3(0.0);
                float diskGlowAcc = 0.0;
                float dopplerBeaming = 1.0;

                // --- Gravitational Raymarching Leapfrog Loop ---
                for (int i = 0; i < 220; i++) {
                    float r2 = dot(p, p);
                    float r = sqrt(r2);
                    
                    // Trap check: Photon crossed the Event Horizon threshold
                    if (r < rs + 0.05) {
                        finalColor = vec3(0.0, 0.0, 0.0);
                        break;
                    }
                    
                    // Boundary escape check: Photon cleared the gravity well completely
                    if (r > 35.0) {
                        finalColor += getBackgroundStars(v);
                        break;
                    }

                    // Relativistic Deflection Physics Formulation (Bending Light Paths)
                    // Acceleration towards singularity = -G * M * position / r^3
                    vec3 gravityAcc = - (3.0 * GM * cross(p, v) * cross(p, v)) / (r2 * r2 * r);
                    gravityAcc += - (GM / (r2 * r)) * p; // Combined Newtonian component fallback
                    
                    v += gravityAcc * dt;
                    v = normalize(v); // Constraints: Light speed consistency c=1
                    
                    vec3 prev_p = p;
                    p += v * dt; // Leap step forward

                    // Accretion Disk intersection checker (Crossed Equatorial zero plane y=0)
                    if (prev_p.y * p.y < 0.0) {
                        float disk_r = length(p.xz);
                        
                        // Disk inner bound and outer bound constraints
                        if (disk_r > rs * 1.3 && disk_r < rs * 5.5) {
                            
                            // Generate fluid dynamics animation for the orbiting plasma
                            float phi = atan(p.z, p.x);
                            float diskNoise = hash(vec3(floor(disk_r * 12.0), floor(phi * 25.0 - u_time * 6.0), 0.0));
                            
                            // Standard hot thermal matter palette mapping
                            vec3 gasColor = vec3(1.0, 0.42, 0.08) * (0.4 + 0.6 * diskNoise);
                            
                            // Relativistic Doppler Beaming Effect Calculation:
                            // Matter rotating towards you gains severe brightness, moving away turns dark.
                            vec3 diskOrbitVel = normalize(vec3(-p.z, 0.0, p.x));
                            float dopplerFactor = dot(v, diskOrbitVel);
                            dopplerBeaming = pow(clamp(1.0 + dopplerFactor * 0.85, 0.1, 2.5), 3.0);
                            
                            float densityProfile = smoothstep(rs * 5.5, rs * 2.5, disk_r) * smoothstep(rs * 1.3, rs * 2.0, disk_r);
                            
                            // Accumulate glowing matter slice values
                            diskGlowAcc += densityProfile * (1.0 / disk_r) * dopplerBeaming;
                            finalColor += gasColor * densityProfile * (1.6 / disk_r) * dopplerBeaming;
                        }
                    }
                }

                // Add diffuse outer core atmosphere glow
                finalColor += vec3(0.95, 0.35, 0.05) * diskGlowAcc * 0.35;

                gl_FragColor = vec4(finalColor, 1.0);
            }
        `;

        // --- 4. Pipeline Geometry Mapping ---
        const geometry = new THREE.PlaneGeometry(2, 2);
        const material = new THREE.ShaderMaterial({
            vertexShader: vertexShader,
            fragmentShader: fragmentShader,
            uniforms: uniforms
        });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // --- 5. Inputs & Interactivity Management ---
        window.addEventListener('resize', () => {
            renderer.setSize(window.innerWidth, window.innerHeight);
            uniforms.u_resolution.value.set(window.innerWidth, window.innerHeight);
        });

        // Click and drag logic for orbital interaction
        window.addEventListener('mousedown', (e) => {
            isDragging = true;
            previousMousePosition = { x: e.clientX, y: e.clientY };
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;

            const deltaX = e.clientX - previousMousePosition.x;
            const deltaY = e.clientY - previousMousePosition.y;

            targetMouseX -= deltaX * 0.003;
            targetMouseY += deltaY * 0.003;

            // Clamping vertical axis boundary locks to prevent flipped orientation glitches
            targetMouseY = Math.max(-0.45, Math.min(0.45, targetMouseY));

            previousMousePosition = { x: e.clientX, y: e.clientY };
        });

        window.addEventListener('mouseup', () => isDragging = false);
        window.addEventListener('mouseleave', () => isDragging = false);

        // Touch support for mobile devices
        window.addEventListener('touchstart', (e) => {
            isDragging = true;
            previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        });

        window.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            const deltaX = e.touches[0].clientX - previousMousePosition.x;
            const deltaY = e.touches[0].clientY - previousMousePosition.y;
            targetMouseX -= deltaX * 0.005;
            targetMouseY += deltaY * 0.005;
            targetMouseY = Math.max(-0.45, Math.min(0.45, targetMouseY));
            previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        });
        window.addEventListener('touchend', () => isDragging = false);

        // --- 6. Execution Animation Loop ---
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);

            // Smooth interpolation (Lerp) for mouse rotations
            uniforms.u_mouse.value.x += (targetMouseX - uniforms.u_mouse.value.x) * 0.1;
            uniforms.u_mouse.value.y += (targetMouseY - uniforms.u_mouse.value.y) * 0.1;

            uniforms.u_time.value = clock.getElapsedTime();
            
            renderer.render(scene, camera);
        }

        animate();
    </script>
</body>
</html> 
























G = 1
c = 1
M = 10








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














import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

G = 1
M = 1
L = 4

def geodesics(phi, y):
    u, up = y
    du_dphi = up
    dup_dphi = (G * M / L ** 2) - u + (3 * G * M * u ** 2)
    return [du_dphi, dup_dphi]

phi_span = (0, 50)
y0 = [0.1, 0]

sol = solve_ivp(geodesics, phi_span, y0, t_eval = np.linspace(0, 50, 5000))

u = sol.y[0]
phi = sol.t
r = 1 / u
x = r * np.cos(phi)
y = r * np.sin(phi)

plt.figure(figsize = (8, 8))
plt.plot(x, y)
plt.scatter(0, 0, color = 'black', label = 'Mass')
plt.axis('equal')
plt.legend()
plt.title("Relativistic Orbit")
plt.show()

